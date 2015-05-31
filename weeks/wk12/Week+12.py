
# coding: utf-8

# # A Quick Introduction to sentiment analysis using TextBlob

# In[ ]:

import math
from textblob import TextBlob


# In[ ]:

text = "Learning storing and retrieving data is essential for data analysis. W205 is a core IR course in the MIDS program"
blob = TextBlob(text)


# Once we have a textblob object, we can do manythings easily

# In[ ]:

blob.tags


# In[ ]:

blob.sentences


# In[ ]:

blob.words


# In[ ]:

blob.words.count("is")


# In[ ]:

doclist = ["The School of Information is both UC Berkeley newest and its smallest school.            Located in the center of campus, the I School is a graduate research and education           community committed to expanding access to information and to improving its usability,            reliability, and credibility while preserving security and privacy. ", "The I School at Berkeley offers two professional master’s degrees and an academic doctoral degree.            Our MIMS program trains students for careers as information professionals and emphasizes            small classes and project-based learning.", "The Master of Information and Data Science (MIDS) program at Berkeley is an innovative part-time fully            online program that trains data-savvy professionals and managers. Working with data at scale            requires distinctive new skills and tools. The MIDS program is distinguished by its disciplinary            breadth; unlike other programs that focus on advanced mathematics and modeling alone,            the MIDS degree provides students insights from social science and policy research,           as well as statistics, computer science and engineering."]


# In[ ]:

word="MIDS"
tf=blob.words.count(word)/float(len(blob.words))
tf


# In[ ]:

DocContain=sum(1 for blob in doclist if word in blob)
DocContain


# In[ ]:

idf=math.log(len(doclist) / float((1 + DocContain)))
idf


# In[ ]:

tf_idf=tf*idf
tf_idf


# In[ ]:

blob.noun_phrases


# In[ ]:

blob.np_counts


# In[ ]:

blob = TextBlob("This is the best book that I have ever read")


# In[ ]:

blob.sentiment


# In[ ]:

blob = TextBlob("This is the best book that I have ever read. The story was truly engaging.")


# In[ ]:

blob.sentences


# In[ ]:




# In[ ]:

for sen in blob.sentences:
    print(sen,sen.sentiment)


# In[ ]:

sen.polarity


# In[ ]:

sen.subjectivity


# In[ ]:

blob.translate(to="es")


# In[ ]:




# In[ ]:




# In[ ]:

from textblob.classifiers import NaiveBayesClassifier

train = [
    ('I love this program.', 'p'),
    ('This is an amazing program!', 'p'),
    ('I met very smart people.', 'p'),
    ('I submitted my best solutions.', 'p'),
    ('I do not like this program', 'n'),
    ('I am tired of w205 stuff.', 'n'),
    ("I can't finish my project", 'n')
]
test = [
    ('The program was awesome.', 'p'),
    ("I can't believe I'm finishing w205.", 'n'),
    ("I feel great!", 'p')
]


# In[ ]:

import time
trainT = time.time()
cl = NaiveBayesClassifier(train)
print "Training took "+str(time.time()-trainT)+" seconds"


# In[ ]:

cl.classify("Berkeley people are amazing")


# In[ ]:

from textblob import TextBlob
blob = TextBlob("Hadoop is amazing. "
                "But writing map-reduce jobs in Java takes time.",
                classifier=cl)


# In[ ]:

blob.classify() 


# In[ ]:

for sen in blob.sentences:
    print(sen, sen.classify())
  


# In[ ]:

cl.accuracy(test)


# In[ ]:




# 
