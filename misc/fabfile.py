__author__ = 'ssatpati'

from fabric.api import *
import time

gpfs1 = '50.97.213.6'
gpfs2 = '50.97.213.3'
gpfs3 = '108.168.236.146'

HOSTS = [gpfs1, gpfs2, gpfs3]
env.user = "root"
#env.key_filename = "/Users/ssatpati/0-DATASCIENCE/DEV/SL/keys/npp/id_rsa"
env.key_filename = "/root/.ssh/id_rsa"

m = 1000000
ZIP_DIR = "/gpfs/gpfsfpo/ngrams"
SCRIPT_DIR = "/gpfs/gpfsfpo/python-data-load-store/misc/"


@task
@parallel
@hosts(gpfs1, gpfs2, gpfs3)
def mumbler_task(word1):
    print("@@@ Executing on %s as %s @@@" % (env.host, env.user))
    run("pwd")
    run("ls -l")
    # Pattern Passed based on FileName to ensure hosts process local files in the order they were downloaded
    if env.host == gpfs1:
        cmd = ["python", "mumbler.py", word1, ZIP_DIR, "0:33", env.host]
        with cd(SCRIPT_DIR):
            run(" ".join(cmd))
    elif env.host == gpfs2:
        cmd = ["python", "mumbler.py", word1, ZIP_DIR, "34:66", env.host]
        with cd(SCRIPT_DIR):
            run(" ".join(cmd))
    elif env.host == gpfs3:
        cmd = ["python", "mumbler.py", word1, ZIP_DIR, "67:99", env.host]
        with cd(SCRIPT_DIR):
            run(" ".join(cmd))
    else:
        raise Exception("Illegal Host, Aborting!!!")


@task
#@runs_once
@hosts(gpfs1)
def aggregate(word1):
    with cd("/gpfs/gpfsfpo"):
        run("du -sm")

    with cd("/gpfs/gpfsfpo/ngrams/output"):
        run("ls -lh")

    cmd = ["python", "mumbler_aggregator.py", word1, ZIP_DIR, ",".join(HOSTS)]
    with cd(SCRIPT_DIR):
        run(" ".join(cmd))

    with cd("/gpfs/gpfsfpo/ngrams/output"):
        return run("tail -1 mumbler_output.txt")


def controller():
    # Initialize
    word1 = "!"
    while word1 is not None or len(word1) != 0:
        s = time.time()
        execute(mumbler_task, word1=word1)
        results = execute(aggregate, word1=word1)
        word1 = results[gpfs1].split("\t")[2]
        e = time.time()
        print("Word: {0}, Time Taken(s): {0}".format(word1, e-s))
        print("Word for Next Iteration: {0}".format(word1))


if __name__ == '__main__':
    controller()