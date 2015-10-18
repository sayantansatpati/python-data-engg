__author__ = 'ssatpati'

from collections import Counter
input_file = '/Users/ssatpati/0-DATASCIENCE/DEV/github/ml/w261/wk4/topUsers_Apr-Jul_2014_1000-words.txt'

categoryCounter = Counter()

with open(input_file, 'r') as f:
    for line in f:
        t = line.strip().split(",")
        categoryCounter.update(t[1])
        print t[0], t[1], t[2], len(t)

print categoryCounter.most_common()

idx = 1
l = [[1.0,2.0,3.0,4.0],[1.5,2.5,3.5,4.5]]
print ",".join(str(i) for i in l[idx])
