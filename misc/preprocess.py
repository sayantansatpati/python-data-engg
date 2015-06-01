__author__ = 'ssatpati'

import glob
import zipfile
import time
import sys
import pickle
import os.path
from collections import defaultdict
import contextlib
from pprint import pprint

ZIP_DIR = "/gpfs/gpfsfpo/ngrams"
ZIP_FILE = "googlebooks-eng-all-2gram-20090715-{0}.csv.zip"

COUNT_KEY = "C-O-U-N-T"
m = 1000000

# Dict word:counts for All Zip Files
dd = defaultdict(lambda: defaultdict(int))

def preproc(pattern, zip_dir=ZIP_DIR):
    # Create the Files to be processed based on Pattern
    t = pattern.split(":")
    f_list = []
    for i in xrange(int(t[0]), int(t[1]) + 1):
        f_list.append(os.path.join(zip_dir, ZIP_FILE.format(i)))

    for g in f_list:
        print(g)
        with contextlib.closing(zipfile.ZipFile(g, "r")) as z:
            # For Each File in the Zip
            for zf in z.filelist:
                cnt = 0
                print("Pre-Processing File: {0}".format(zf.filename))
                match = False

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
                            dd[bigram[0]][COUNT_KEY] += 1
                            if len(bigram) == 2:
                                    dd[bigram[0]][bigram[1]] += int(tokens[2])
                        except Exception as e:
                                print line
                                print e

                        cnt += 1
                        if cnt % m == 0:
                            print("No. of lines read in file {0}: {1}]".format(zf.filename, cnt))
                            print("DefaultDict(counts), Length: {0}, Size: {1}".format(len(dd), sys.getsizeof(dd)))


if __name__ == '__main__':
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    if len(sys.argv) < 4:
        raise Exception("Illegal Number of Arguments Passed: " + len(sys.argv))

    preproc(pattern=sys.argv[1], zip_dir=sys.argv[2])
