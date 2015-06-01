__author__ = 'ssatpati'

import os
import sys
import pickle
import pprint
from collections import defaultdict
from itertools import chain
import random


ZIP_DIR = "/gpfs/gpfsfpo/ngrams"
OUT_DIR = "output"
OUT_FILE = "mumbler_output.txt"


def aggregate(word1, hosts, zip_dir=ZIP_DIR):
    l = []
    for h in hosts.split(","):
        f_name = "".join([h, "_counts.p"])
        l.append(pickle.load(open(os.path.join(ZIP_DIR, OUT_DIR, f_name))))

    dd_merged = defaultdict(int)
    for k,v in chain(l[0].iteritems(), l[1].iteritems(), l[2].iteritems()):
        dd_merged[k] += v

    #pprint.pprint(dd_merged)
    print("Cross Checking Counts of Word: {0}".format(word1))
    print(l[0].get(word1))
    print(l[1].get(word1))
    print(l[2].get(word1))
    print(dd_merged.get(word1))
    assert l[0].get(word1) + l[1].get(word1) + l[2].get(word1) == dd_merged.get(word1)

    random_key = random.choice(dd_merged.keys())
    random_key_value = dd_merged.get(random_key)
    probability = (random_key_value * 1.0)/dd_merged.get(word1)
    print("Random Key: {0}, Value: {1}, Probability: {2}".format(random_key,
                                                                 random_key_value,
                                                                 probability))

    # Write to Output File
    with open(os.path.join(ZIP_DIR, OUT_DIR, OUT_FILE), "w") as f:
        f.write("%s\t%s\t%s\t%s\t%s" %(word1, dd_merged.get(word1), random_key, random_key_value, probability))


if __name__ == '__main__':
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    if len(sys.argv) < 4:
        raise Exception("Illegal Number of Arguments Passed: " + len(sys.argv))

    aggregate(word1=sys.argv[1], zip_dir=sys.argv[2], hosts=sys.argv[3])
