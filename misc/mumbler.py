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

OUT_DIR = "output"
ZIP_DIR = "/gpfs/gpfsfpo/ngrams"


m = 1000000
ZIP_FILE = "googlebooks-eng-all-2gram-20090715-{0}.csv.zip"


def mumbler(word1, pattern, zip_dir=ZIP_DIR):
    # Create the Files to be processed based on Pattern
    t = pattern.split(":")
    f_list = []
    for i in xrange(int(t[0]), int(t[1]) + 1):
        f_list.append(os.path.join(zip_dir, ZIP_FILE.format(i)))

    # Dict word:counts for All Zip Files
    dd = defaultdict(int)

    # All Zips in this Dir
    #glob_pattern = ["googlebooks-eng-all-2gram-20090715-", pattern, ".csv.zip"]
    #zip_pattern = os.path.join(zip_dir, "".join(glob_pattern))
    #print("ZIP File Pattern: {0}".format(zip_pattern))

    for g in f_list;
    #for g in glob.glob(zip_pattern):
        print(g)
        with contextlib.closing(zipfile.ZipFile(g, "r")) as z:
        #with zipfile.ZipFile(g) as z:
            # For Each File in the Zip
            for zf in z.filelist:
                cnt = 0
                print("Processing File: {0} for Word: {1}".format(zf.filename, word1))
                match = False

                # Open file
                with contextlib.closing(z.open(zf)) as f:
                #with z.open(zf) as f:
                    # For Each line in File
                    for line in f:
                        bigram = line.split("\t")[0].split()
                        #print bigram

                        # Ignore Empty Bigrams or if Bigram doesn't start with passed argument
                        if not bigram or len(bigram) == 0:
                            continue

                        if word1 != bigram[0]:  # Doesn't match
                            if match:  # Previously Matched
                                break # Next File
                            else:
                                continue
                        else:  # Same w1; Populate Dict
                            match = True # Match Found
                            try:
                                if len(bigram) == 2:
                                    dd[bigram[0]] += 1
                                    dd[bigram[1]] += 1
                                else:
                                    dd[bigram[0]] += 1
                            except Exception as e:
                                print line
                                print bigram
                                print e
                                sys.exit(0)

                        cnt += 1
                        if cnt % m == 0:
                            print("No. of lines read in file {0}: {1}]".format(zf.filename, cnt))
    return dd


if __name__ == '__main__':
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    if len(sys.argv) < 5:
        raise Exception("Illegal Number of Arguments Passed: " + len(sys.argv))

    #Output Directory
    output_dir = os.path.join(sys.argv[3], OUT_DIR)
    if os.path.exists(os.path.join(sys.argv[3], OUT_DIR)):
        os.makedirs(output_dir)

    s = time.time()
    # Invoke Mumbler
    dd = mumbler(word1=sys.argv[1], zip_dir=sys.argv[2], pattern=sys.argv[3])
    # Pickle Dump
    pickle.dump(dd, open(os.path.join(output_dir, sys.argv[4] + "_counts.p"), "wb"))
    e = time.time()
    print("Time Taken(m): {0}".format(e-s))
