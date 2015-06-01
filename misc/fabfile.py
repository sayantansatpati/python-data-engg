__author__ = 'ssatpati'

from fabric.api import *

import pprint
import glob
import zipfile
import time
import sys
from collections import defaultdict
from pprint import pprint

gpfs1 = '50.97.213.6'
gpfs2 = '50.97.213.3'
gpfs3 = '108.168.236.146'

env.hosts = [gpfs1, gpfs2, gpfs3]
env.user = "root"
#env.key_filename = "/Users/ssatpati/0-DATASCIENCE/DEV/SL/keys/npp/id_rsa"
env.key_filename = "/root/.ssh/id_rsa"

m = 1000000
ZIP_DIR = "/gpfs/gpfsfpo/ngrams"
SCRIPT_DIR = "/gpfs/gpfsfpo/python-data-load-store/misc/"

@task
@parallel
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
@runs_once
def aggregate(word1):
    with cd("/gpfs/gpfsfpo/ngrams/output"):
        run("ls -l")

    cmd = ["python", "mumbler_aggregator.py", word1, ZIP_DIR, ",".join(env.hosts)]
    with cd(SCRIPT_DIR):
        run(" ".join(cmd))


def controller():
    execute(mumbler_task, word1="!")
    execute(aggregate, word1="!")

if __name__ == '__main__':
    controller()