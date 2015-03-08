#!/usr/bin/env python
__author__ = 'ssatpati'

import sys
from difflib import SequenceMatcher
from nltk import *
from nltk.corpus import stopwords
import pprint
from datetime import datetime

# NLTK
os.environ["NLTK_DATA"] = "/home/cloudera/nltk_data"
sw = stopwords.words('english')

DATE_TIME_FORMAT = "%Y-%m-%d"

CACHE_FILE = "artist_band.txt"

'''
Dictionary to hold the master list of artist/band names
Will be loaded by each mapper for mapper side join (Distributed Cache)
'''
dict_artist = {}


def tokenize_stem(word):
    """Tokenize, Remove Stop Words, and Stem each word"""
    tokenizer = RegexpTokenizer(r'\w+')
    ls = LancasterStemmer()
    # Tokenize
    tkns = [t for t in tokenizer.tokenize(word) if t.lower() not in sw]
    # Stem
    tkns = [ls.stem(t) for t in tkns]
    # Sort
    tkns = sorted(tkns)
    return tuple(tkns)

with open(CACHE_FILE) as f:
    for l in f:
        l = l.strip()
        dict_artist[tokenize_stem(l)] = l

# input comes from STDIN (standard input)
for line in sys.stdin:
    try:
        # remove leading and trailing whitespace
        line = line.strip()
        # split the line into tokens
        tokens = line.split('\t')

        '''
        # Load master list of artist/band names
        if tokens and len(tokens) == 1:
            dict_artist[tokenize_stem(tokens[0])] = tokens[0]
        '''

        if len(tokens) == 3:
            key = tokenize_stem(tokens[0])
            value = dict_artist.get(key)
            if value is not None:
                dt = datetime.fromtimestamp(long(tokens[1])).strftime(DATE_TIME_FORMAT)
                print("{0}^{1}^{2}^{3}".format(key, dt, value, tokens[2]))
    except:
        print("[Mapper] Ignoring record: {0}".format(line))
        pass

#pprint.pprint(dict_artist)
