__author__ = 'ssatpati'


from nltk import *
from nltk.corpus import stopwords
import pprint
import os

os.environ["NLTK_DATA"] = "/Users/ssatpati/nltk_data"


def build_inverted_index():
    idx = {}
    count = 0
    with open("/Users/ssatpati/nltk_data//corpora/inaugural/1789-Washington.txt") as f:
        lines = f.readlines()
        for line in lines:
            count += 1
            sw = stopwords.words('english')
            tokenizer = RegexpTokenizer(r'\w+')
            for t in tokenizer.tokenize(line):
                if t.lower() not in sw:
                    if idx.get(t) is None:
                        idx[t] = [count]
                    else:
                        idx[t].append(count)
    pprint.pprint(idx)


if __name__ == '__main__':
    '''Main Point of Entry to Program'''
    build_inverted_index()
