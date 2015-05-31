__author__ = 'ssatpati'

import os
import sys
import pickle
import pprint
from collections import defaultdict
from itertools import chain

OUT_DIR = "output"
ZIP_DIR = "/gpfs/gpfsfpo/ngrams"


def aggregate(hosts, zip_dir=ZIP_DIR):
    l = []
    for h in hosts.split(","):
        f_name = "".join([h, "_counts.p"])
        l.append(pickle.load(open(os.path.join(ZIP_DIR, OUT_DIR, f_name))))

    dd_merged = defaultdict(int)
    for k,v in chain([dd.iteritems() for dd in l]):
        dd_merged[k].update(v)

    pprint.pprint(dd_merged)


if __name__ == '__main__':
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    if len(sys.argv) < 3:
        raise Exception("Illegal Number of Arguments Passed: " + len(sys.argv))

    aggregate(zip_dir=sys.argv[1], hosts=sys.argv[2])
