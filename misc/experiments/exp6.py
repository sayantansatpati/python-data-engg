__author__ = 'ssatpati'


d = {'a': 1, 'b': 2, 'c': 3}

if 'a' in d:
    print '1. Yayyyy'


if 'a' in d.keys():
    print '2. Yayyyy'

if 1 in d:
    print '3. Yayyyy'

if 1 in d.values():
    print '4. Yayyyy'

word = 'POPE'
word = word[:-1]
print word
print word

for i in range(len(word)):
    bucket = word[:i] + '_' + word[i+1:]
    print bucket