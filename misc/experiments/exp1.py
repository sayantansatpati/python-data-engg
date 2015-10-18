__author__ = 'ssatpati'

import re
import itertools
line = 'FRO11987 ELE17451 ELE89019 SNA90258 GRO99222'

items = re.split(r'\s', line)

print items
items.sort()
print items

l = len(items)

for i in xrange(l):
    print '%s\t%d' %(items[i], 1)
    for j in xrange(i + 1, l):
        print'%s,%s\t%d' %(items[i],items[j],1)

for c in itertools.combinations(items, 1):
    print '%s\t%d' %(c[0], 1)
    for c in itertools.combinations(items, 2):
        print '%s,%s\t%d' %(c[0],c[1], 1)
for c in itertools.combinations(items, 3):
    print '%s,%s,%s\t%d' %(c[0],c[1],c[2], 1)


d1 = {'a': 20, 'b': 30, 'c': 40}
d2 = {'a': 21, 'b': 31, 'c': 41}
d3 = {'a': 22, 'b': 32, 'c': 42}

d_merged = {}
for d in d1, d2, d3:
    for k, v in d.iteritems():
        print k,v
        d_merged[k] = d_merged.get(k, 0) + v
    print d_merged.items()

d_final = {}
for k,v in d_merged.iteritems():
    print k,v
    if v >= 90:
        d_final[k] = v

print d_final.items()