__author__ = 'ssatpati'


import os
import io
from whoosh import *
from whoosh.fields import Schema
from whoosh.fields import ID, KEYWORD, TEXT
from whoosh.index import create_in
from whoosh.index import open_dir
import glob
import codecs


def create_index():
    my_schema = Schema(id = ID(unique=True, stored=True),
                    path = ID(stored=True),
                    source = ID(stored=True),
                    author = TEXT(stored=True),
                    title = TEXT(stored=True),
                    year = TEXT(stored=True),
                    text = TEXT)

    if not os.path.exists("1-index"):
        os.mkdir("1-index")
        index = create_in("1-index", my_schema)

    index = open_dir("1-index")
    writer = index.writer()


    for name in glob.glob('/Users/ssatpati/nltk_data/corpora/gutenberg/*.txt'):
        #print(name)
        with codecs.open(name, 'r', encoding='utf8') as f:
            h = f.readlines()[0].replace("[", "").replace("]", "")
            t = "NA"
            a = "NA"
            y = "NA"
            if "by" in h:
                title = "".join(h.split("by")[0])
                h1 = h.split("by")[1].split()
                if h1[len(h1)-1].isdigit():
                    a = "".join(h1[0:len(h1)-1])
                    y = h1[len(h1)-1]
                else:
                    a = "".join(h1)
            else:
                a = h
            print(t, a, y)

            writer.add_document(id = name,
                    path = os.path.basename(name),
                    source = unicode(name),
                    author = unicode(a),
                    title = unicode(t),
                    year = unicode(y),
                    text = io.open(name, encoding='utf-8').read())


if __name__ == '__main__':
    create_index()
