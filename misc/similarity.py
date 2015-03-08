__author__ = 'ssatpati'

from difflib import SequenceMatcher
from nltk import *
from nltk.corpus import stopwords

os.environ["NLTK_DATA"] = "/Users/ssatpati/nltk_data"
sw = stopwords.words('english')

list_words = ["The Doors",
                "Doors, The",
                "Ben Harper & The Innocent Criminals",
                "Ben Harper and the Innocent Criminals",
                "Foo Fighters",
                "The Foo Fighters",
                "Foo Bar Fighters"]


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def similar2():
    tokenizer = RegexpTokenizer(r'\w+')
    ls = LancasterStemmer()
    for l in list_words:
        # Tokenize
        tokens = [t for t in tokenizer.tokenize(l) if t.lower() not in sw]
        # Stem
        tokens = [ls.stem(t) for t in tokens]
        # Sort
        tokens = sorted(tokens)
        print(tokens)


if __name__ == '__main__':
    #print(similar(s1, s2))
    similar2()


