__author__ = 'ssatpati'

import nltk
from nltk.corpus import inaugural
import os
import math

tokens = ['providential', 'citizens']
docs = ['1789-Washington.txt','1797-Adams.txt','1801-Jefferson.txt']
os.environ["NLTK_DATA"] = "/Users/ssatpati/nltk_data"

def tf_idf():
    for token in tokens:
        tf_list = []
        for doc in docs:
            words = inaugural.words(doc)
            term_freq = tf(token, words)
            tf_list.append(term_freq)
            print("TF for token '{0}' in '{1}': {2}".format(token, doc, term_freq))
        print(tf_list)
        tfidf = sum(tf_list) * idf(token)
        print("### TF-IDF: {0}".format(tfidf))


def tf(token, words):
    n = len([True for w in words if w == token])
    term_freq = float(n)/len(words)
    return term_freq


def idf(token):
    nd = 0;
    for doc in docs:
        words = inaugural.words(doc)
        if token in words:
            nd += 1
    idf = 0;
    try:
        idf = math.log(float(len(docs)) / nd);
    except ZeroDivisionError as zde:
        print(zde)
    print("IDF {0}".format(idf))
    return idf


if __name__ == '__main__':
    tf_idf()