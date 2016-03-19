from tables.index import opt_search_types

__author__ = 'ssatpati'


import sys
import json
import elasticsearch
from elasticsearch import helpers
import pprint
import numpy as np
import sklearn.feature_extraction.text as text
import lda

es = elasticsearch.Elasticsearch(hosts='54.183.182.71')

q = {
"query" : {
    "filtered": {
        "filter": {
          "and": [
            {
              "term" : { "state" : "nv" }
            },
            {
              "term" : { "city" : "vegas" }
            }
          ]
        }
    }
},
"aggs" : {
        "state" : {
            "terms" : {
              "field" : "state"
            },
            "aggs": {
                "city": {
                   "terms": {
                      "field": "city"
                   },
                   "aggs": {
                      "neighborhoods": {
                         "terms": {
                            "field": "neighborhoods"
                         },
                         "aggs": {
                            "stars": {
                               "terms": {
                                  "field": "stars"
                               }
                            }
                        }
                      }
                  }
                }
            }
        }
    }
}

# Returns 10 records by default
res = es.search(index="yelp", doc_type="business", body=q)
print pprint.pprint(res['hits']['hits'][0])
print("%d Businesses found in NV, Vegas" % res['hits']['total'])
pprint.pprint(res['hits']['hits'][0]['_source']['business_id'])

business_ids = [hit['_source']['business_id'] for hit in res['hits']['hits']]

# Explore 1 business

q = {
        "query":
            {
                "match":
                    {
                        "business_id": business_ids[0]
                    }
            }
    }

res = es.search(index="yelp", doc_type="review", body=q, search_type='count')
print pprint.pprint(res)

res_total = res['hits']['total']
res_from = 0
res_size = 20
doc_cnt = 0

doc_titles = []
content = []
stars = []
while res_from < res_total:
    print 'Total: {0}, From: {1}'.format(doc_cnt, res_from)
    res = es.search(index="yelp", doc_type="review", body=q, from_=res_from, size=res_size)

    for hit in res['hits']['hits']:
        content.append(hit['_source']['text'])
        stars.append(hit['_source']['stars'])
        doc_titles.append((hit['_source']['review_id'], hit['_source']['stars'], hit['_source']['text']))
        doc_cnt += 1

    res_from += res_size

print 'Length: ', len(content)

cv = text.CountVectorizer(stop_words='english', min_df=10)
term_doc_matrix = cv.fit_transform(content)

tfidf = text.TfidfVectorizer(stop_words='english', min_df=10)
tfidf.fit_transform(content)

cv_vocab = sorted(cv.vocabulary_.items(), key=lambda x: -x[1])

print "\n### CV Vocab:\n"
print cv_vocab


tfidf_vocab = []
for i in xrange(len(tfidf.idf_)):
    tfidf_vocab.append((tfidf.get_feature_names()[i], tfidf.idf_[i]))

print "\n### TF-IDF Vocab:\n"
print tfidf_vocab

print sum([s for s in stars])
print sum([s for s in stars]) * 1.0 / doc_cnt

print cv.vocabulary_
print term_doc_matrix


num_topics = 10

#LDA
model = lda.LDA(n_topics=num_topics, n_iter=500, random_state=1)
model.fit(term_doc_matrix)

# Topic-Word
topic_word = model.topic_word_
print("type(topic_word): {}".format(type(topic_word)))
print("shape: {}".format(topic_word.shape))

for n in range(num_topics):
    sum_pr = sum(topic_word[n,:])
    print("topic: {} sum: {}".format(n, sum_pr))

print "\n\n"
n = 5
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(cv.vocabulary_.keys())[np.argsort(topic_dist)][:-(n+1):-1]
    print('*Topic {}\n- {}'.format(i, ' '.join(topic_words)))

print "\n\n"

#Doc-Topic
doc_topic = model.doc_topic_
print("type(doc_topic): {}".format(type(doc_topic)))
print("shape: {}".format(doc_topic.shape))

for n in range(num_topics):
    sum_pr = sum(doc_topic[n,:])
    print("document: {} sum: {}".format(n, sum_pr))

print "\n\n"

for n in range(20):
    topic_most_pr = doc_topic[n].argmax()
    print("doc: {} topic: {}\n{}...".format(n,
                                            topic_most_pr,
                                            doc_titles[n][:50]))
