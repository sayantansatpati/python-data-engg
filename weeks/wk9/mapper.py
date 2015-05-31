#!/usr/bin/env python
import sys

w_counts = {}

# input comes from STDIN (standard input)
for line in sys.stdin:
    words = line.strip().split()
    for word in words:
        #w_counts[word] = w_counts.get(word, 0) + 1
        print word + "\t" + str(1)

#print(w_counts)
