__author__ = 'ssatpati'

import csv
import pymongo
from pymongo import MongoClient
import collections


# MongoDB Client & DB
client = MongoClient('mongodb://localhost:27017/')
db = client['cong_db']
coll = db['mem_db']

def load():
    records = csv.DictReader(open("legislators-historic.csv"))
    #sample = list(records)
    #print(sample[1])

    try:
        for record in list(records):
            coll.insert(record)
    except Exception as e:
        print("### Exception: ", e)

def find():
    print(coll.find_one({"last_name": "Maclay"}))
    print("Total Number : ", coll.count())
    print("members who are woman but not democrat", coll.find({'gender' : 'F', 'party' : {'$ne' : 'Democrat'}}).count())
    for c1 in coll.find({'gender': 'F', 'party': {'$ne': 'Democrat'}}, {'last_name': '1', 'first_name': '1', 'birthday': '1'}):
        print(c1)

    for c2 in coll.find({'party': 'Democrat'}).sort('birthday', -1).limit(1):
        print("Youngest : ", c2)

    for c3 in coll.find({'$or':[ {'first_name': 'john'}, {'first_name': 'Joshua'}] }):
        print(c3)

    fd = collections.OrderedDict()
    ld = collections.OrderedDict()
    for c4 in coll.find({}, {'last_name': '1', 'first_name': '1'}):
        ld[c4['last_name']] = ld.get(c4['last_name'], 0) + 1
        fd[c4['first_name']] = fd.get(c4['first_name'], 0) + 1
        '''
        if c4['last_name'] not in ld:
            ld[c4['last_name']] = 1
        else:
            ld[c4['last_name']] = ld.get(c4['last_name']) + 1
        if c4['first_name'] not in fd:
            fd[c4['first_name']] = 1
        else:
            fd[c4['first_name']] = fd.get(c4['first_name']) + 1
        '''
    print("Most Frequent Last Name", (ld.items())[0])
    print("Most Frequent First Name", (fd.items())[0])

if __name__ == '__main__':
    #load()
    find()
