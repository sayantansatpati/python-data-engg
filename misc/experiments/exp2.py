__author__ = 'ssatpati'

import re
import itertools

item_set_1 = {}
item_set_2 = {}

max_basket_len = 0

with open('ProductPurchaseData.txt', 'r') as f:
    for line in f:
        line.strip()
        items = re.split(r'\s', line)
        items.sort()

        if len(items) > max_basket_len:
            max_basket_len = len(items)
            if max_basket_len == 39:
                print line

        for i in items:
            item_set_1[i] = item_set_1.get(i, 0) + 1

        for c in itertools.combinations(items, 2):
            key = '{0},{1}'.format(c[0], c[1])
            item_set_2[key] = item_set_2.get(key, 0) + 1

print 'Max Basket Len: %d' %(max_basket_len)
print 'Total Unique Keys: %d' %(len(item_set_1))

total_item_set_1 = 0
for k,v in item_set_1.iteritems():
    if v > 100:
        total_item_set_1 += 1
print 'Total Item Set of Size 1: %d' %(total_item_set_1)

total_item_set_2 = 0
for k,v in item_set_2.iteritems():
    items = re.split(r',', k)
    if item_set_1.get(items[0], 0) > 100 and item_set_1.get(items[1], 0) > 100 and v > 100:
        total_item_set_2 += 1
print 'Total Item Set of Size 2: %d' %(total_item_set_2)