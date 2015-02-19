
# coding: utf-8

# ##NLTK is extensively documented and 
# ##you should not have hard time finding the thing you want to do

# In[1]:

from nltk.book import *


# 
# DT	determiner
# JJ	adjective
# JJR	adjective, comparative	
# JJS	adjective, superlative
# NN	noun, singular
# NNS	noun plural
# NNP	proper noun, singular
# PRP	personal pronoun
# RB	adverb
# VB	verb
# WDT	wh-determiner

# ## Tokenizing a text
# 

# In[11]:

myText = ["It is really good", "I do not like it"]


# In[12]:

from nltk.tokenize import word_tokenize
tokens = [word_tokenize(txt) for txt in myText]
print tokens


# ##Finding part of speach 

# In[13]:


speechTag=nltk.pos_tag(tokens[0])
speechTag


# ##Chunking and ne_chunk

# In[23]:

print nltk.ne_chunk(speechTag)


# ## Working with sample texts

# In[18]:

mobyText = nltk.text.Text(nltk.corpus.gutenberg.words('melville-moby_dick.txt'))


# Distributional similarity: words that that occur frequently in the same context and with a similar distribution

# In[19]:

mobyText.similar("whale")


# You can display graphs and charts that can show dispersions and frequency

# In[22]:

guten = nltk.text.Text(nltk.corpus.gutenberg.words())
guten.dispersion_plot(["sea", "whale", "ship", "crew"])


# ##Name_entity for sentiment analysis (who is this sentence about)
# 

# In[ ]:



