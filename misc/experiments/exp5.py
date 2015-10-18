__author__ = 'ssatpati'
import ast
from sets import Set
import urllib2

'''
with open('/Users/ssatpati/0-DATASCIENCE/DEV/github/ml/w261/wk5/stripes.txt', 'r') as f:
    d = {}
    for line in f:
        t = line.strip().split('\t')
        d[t[0]] = ast.literal_eval(t[1])

    #print d.items()
'''

d1 = {'a': 10, 'b': 20, 'c': 30}
d2 = {'a': 10, 'b': 20, 'e': 30}

s1 = Set(d1.keys())
s2 = Set(d2.keys())

print s1.intersection(s2)
print s1.difference(s2)
print s2.difference(s1)

str1 = 'abc'
str2 = 'xyz'

print str1 >= str2
print str1 < str2

d = {}
f = urllib2.urlopen("https://s3-us-west-2.amazonaws.com/ucb-mids-mls-sayantan-satpati/hw54/word_cooccur/frequent_stripes.txt")
for line in f.readlines():
    tokens = line.strip().split('\t')
    d[tokens[0].replace("\"","")] = ast.literal_eval(tokens[1])

print len(d)