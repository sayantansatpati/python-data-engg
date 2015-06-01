__author__ = 'ssatpati'

import os
import sys
import pickle
import pprint
from collections import defaultdict
from itertools import chain

OUT_DIR = "output"
ZIP_DIR = "/gpfs/gpfsfpo/ngrams"


def aggregate(word1, hosts, zip_dir=ZIP_DIR):
    l = []
    for h in hosts.split(","):
        f_name = "".join([h, "_counts.p"])
        l.append(pickle.load(open(os.path.join(ZIP_DIR, OUT_DIR, f_name))))

    dd_merged = defaultdict(int)
    for k,v in chain(l[0].iteritems(), l[1].iteritems(), l[2].iteritems()):
        dd_merged[k] += v

    pprint.pprint(dd_merged)
    print(l[0].get(word1))
    print(l[1].get(word1))
    print(l[2].get(word1))
    print(dd_merged.get(word1))


if __name__ == '__main__':
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    if len(sys.argv) < 4:
        raise Exception("Illegal Number of Arguments Passed: " + len(sys.argv))

    aggregate(word1=sys.argv[1], zip_dir=sys.argv[2], hosts=sys.argv[3])
