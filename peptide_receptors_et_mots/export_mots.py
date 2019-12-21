from pymongo import MongoClient
import pprint
import collections

client = MongoClient()
db = client.proteins

mots = db.archea_mots

all = [i for i in mots.find()]

list_of_mots = []

for case in all:
    for i in case['mots']:
        for mot in i['mots']:
            list_of_mots.append(mot)

c = collections.Counter()

for i in list_of_mots:
    c[i]+=1

pprint.pprint(c)

with open('/Users/liquidbrain/Desktop/mots9.csv', 'w') as file:
    file.write('Mots;length;number\n')
    for key, value in c.items():
        file.write('{};{};{}\n'.format(key, len(key), value))