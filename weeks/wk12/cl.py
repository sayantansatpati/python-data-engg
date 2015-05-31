from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import sys
import os.path
import pickle
import time

CLASSIFIER_PICKLE = "classifier.p"

def train_classifier():
    train = []

    with open("Dataset.txt") as f:
        lines = f.readlines()
        #cl = NaiveBayesClassifier(lines)
        for line in lines:
            blob = TextBlob(line)
            try:
                for sentence in blob.sentences:
                    pl = sentence.sentiment.polarity
                    s = None
                    if pl > 0:
                        s = "pos"
                    else:
                        s = "neg"
                    train.append((line, s))
                    #print(line, s)
            except:
                pass


    print("Start Training Classifier...")
    trainT = time.time()
    cl = NaiveBayesClassifier(train)
    print "Training took " + str(time.time() - trainT) + " seconds"
    pickle.dump(cl, open(CLASSIFIER_PICKLE, "wb"))
    print("Dumped Classifier...")
    return cl


def classify(cl):
    print("Classifying contents of test-dataset.txt")
    with open("test-dataset.txt") as f:
        lines = f.readlines()
        for line in lines:
            blob = TextBlob(line, classifier=cl)
            blob.classify()
            try:
                for s in blob.sentences:
                    print(s, s.classify())
            except:
                pass

if __name__ == '__main__':
    cl = None
    if os.path.isfile(CLASSIFIER_PICKLE):
        print("Classifier Pickle File Exists...")
        cl = pickle.load(open(CLASSIFIER_PICKLE, "rb"))
    else:
        print("Training Classifier For the first time...")
        cl = train_classifier()
    classify(cl)