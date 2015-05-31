#!/usr/bin/env python

import sys

last_word = None
word_count = 0

for line in sys.stdin:

    line = line.strip()
    word, count = line.split("\t")

    count = int(count)
    if not last_word:
        last_word = word

    if word == last_word:
        word_count += count
    else:
        result = [last_word, word_count]
        print("\t".join(str(v) for v in result))
        last_word = word
        word_count = 1

print("\t".join(str(v) for v in [last_word, word_count]))
