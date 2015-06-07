__author__ = 'ssatpati'

import glob
import zipfile
import time
import sys
import os.path
from collections import defaultdict
import contextlib
import multiprocessing

ZIP_DIR = "/gpfs/gpfsfpo/ngrams"
ZIP_FILE = "googlebooks-eng-all-2gram-20090715-{0}.csv.zip"

COUNT_KEY = "C-O-U-N-T"
m = 1000000


def populate_counts(pattern, zip_dir=ZIP_DIR):
    s = time.time()

    zip_file = os.path.join(zip_dir, ZIP_FILE.format(pattern))
    print "[{0}] Processing Zip File: {1}".format(pattern, zipfile)

    # Dict word:counts for Each Zip File
    dd = defaultdict(lambda: defaultdict(int))

    # Create out file
    out_file = os.path.join(zip_dir, os.path.splitext(os.path.basename(zip_file))[0] + ".txt")
    print(out_file)

    try:
        if os.path.exists(out_file):
            os.remove(out_file)
    except OSError:
        pass

    with contextlib.closing(zipfile.ZipFile(zip_file, "r")) as z:
        # For Each File in the Zip
        for zf in z.filelist:
            cnt = 0
            print("[{0}]Pre-Processing File: {1}".format(pattern, zf.filename))

            # Open file
            with contextlib.closing(z.open(zf)) as f:

                # For Each line in File
                for line in f:
                    tokens = line.split("\t")
                    bigram = tokens[0].split()

                    # Ignore Empty Bigrams or if Bigram doesn't start with passed argument
                    if not bigram or len(bigram) == 0:
                        continue

                    try:
                        dd[bigram[0]][COUNT_KEY] += int(tokens[2])
                        if len(bigram) == 2:
                                dd[bigram[0]][bigram[1]] += int(tokens[2])
                    except Exception as e:
                            print line
                            print e

                    cnt += 1
                    if cnt % m == 0:
                        print("[{0}] No. of lines read in file {1}: {2}]".format(pattern, zf.filename, cnt))
                        print("[{0}] DefaultDict(counts), Length: {1}, Size: {2}".format(pattern, len(dd), sys.getsizeof(dd)))
                        e = time.time()
                        print("[{0}] Time Taken(s) so far: {1}".format(pattern, (e-s)))

                    # For Test
                    #if cnt > (5 * m):
                    #    return

    with open(out_file, "a") as out:
        # Persisting counts to Disk
        print("[{0}] Persisting Counts to Disk for File: {1}".format(pattern, out_file))
        # Write results
        for k, v in sorted(dd.iteritems()):
            for k1, v1 in sorted(v.iteritems()):
                # Next write W2: W1<TAB>W2<TAB>COUNT
                if k1 != COUNT_KEY: # No need to write the COUNT KEY Again
                    out.write("%s\t%s\t%s\n" %(k, k1, v1))


if __name__ == '__main__':
    s = time.time()
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    if len(sys.argv) < 3:
        raise Exception("Illegal Number of Arguments Passed: " + len(sys.argv))

    jobs = []
    t = sys.argv[1].split(":")
    for i in xrange(int(t[0]), int(t[1]) + 1):
        p = multiprocessing.Process(target=populate_counts, args=(i, sys.argv[2]))
        jobs.append(p)
        p.start()

    for job in jobs:
        job.join()

    e = time.time()
    print("TOTAL TIME TAKEN (mins): {0}".format((e-s)/60))

