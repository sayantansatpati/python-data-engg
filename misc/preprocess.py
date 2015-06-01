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

def populate_counts(pattern, zip_dir=ZIP_DIR):
    s = time.time()
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
                            dd[bigram[0]][COUNT_KEY] += int(tokens[2])
                            if len(bigram) == 2:
                                    dd[bigram[0]][bigram[1]] += int(tokens[2])
                        except Exception as e:
                                print line
                                print e

                        cnt += 1
                        if cnt % m == 0:
                            print("No. of lines read in file {0}: {1}]".format(zf.filename, cnt))
                            print("DefaultDict(counts), Length: {0}, Size: {1}".format(len(dd), sys.getsizeof(dd)))
                            e = time.time()
                            print("Time Taken(s) so far: {0}".format(e-s))

                        # For Test
                        #if cnt > (5 * m):
                        #    return


def persist_counts(out_dir, zip_dir=ZIP_DIR):
    # Create Output Directory
    output_dir = os.path.join(zip_dir, out_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_dict = {}

    try:
        # Populate File Dict with file handlers for each ascii bucket: < 37, 37-47, 47-57...
        file_dict[0] = open(os.path.join(zip_dir, out_dir, str(0)), "a")
        f_name = 37
        while f_name <= 127: # ascii range
            file_dict[f_name] = open(os.path.join(zip_dir, out_dir, str(f_name)), "a")
            f_name += 10

        # Write results
        for k, v in dd.iteritems():
            ascii = ord(k[0])
            #print(ascii, k, k1, v1)
            file_handler = file_handler_key(ascii)
            # First write W1: W1<TAB>COUNT
            file_dict[file_handler].write("%s\t%s\n" %(k, v[COUNT_KEY]))
            for k1, v1 in v.iteritems():
                # Next write W2: W1<TAB>W2<TAB>COUNT
                if k1 != COUNT_KEY: # No need to write the COUNT KEY Again
                    file_dict[file_handler].write("%s\t%s\t%s\n" %(k, k1, v1))
    except Exception as e:
        print e
        raise
    finally:
        for k, v in file_dict.iteritems():
            v.close()



def file_handler_key(ascii):
    if ascii <= 37:
        return 37
    elif ascii <= 47:
        return 47
    elif ascii <= 57:
        return 57
    elif ascii <= 67:
        return 67
    elif ascii <= 77:
        return 77
    if ascii <= 87:
        return 87
    elif ascii <= 97:
        return 97
    elif ascii <= 107:
        return 107
    elif ascii <= 117:
        return 117
    elif ascii <= 127:
        return 127
    else: # All Others
        return 0



if __name__ == '__main__':
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    if len(sys.argv) < 4:
        raise Exception("Illegal Number of Arguments Passed: " + len(sys.argv))

    populate_counts(pattern=sys.argv[1], zip_dir=sys.argv[2])
    persist_counts(zip_dir=sys.argv[2], out_dir=sys.argv[3])