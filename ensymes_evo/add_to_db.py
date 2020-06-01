from pymongo import MongoClient
import pprint
from modules import seq_liner_short as sl
import collections

#db init
client = MongoClient()
db = client.proteins
mots = db.mots_v3
enz = db.enzymes

all_mots = [i for i in mots.find()]

#create_new_db_obj
# obj = {
#     "name": 'Orexin',
#     'mots': []
# }
name = "APP"

old = enz.find_one({'name': name})
obj = enz.find_one({'name': name})

for i in all_mots[0:2]:
    new_obj = {
        'mot': i['mot'],
        'finds': i['finds'],
        'alt_mots': i['alt_mots']
    }
    obj['mots'].append(new_obj)

pprint.pprint(obj)

enz.replace_one(old, obj)
# enz.insert_one(obj)

