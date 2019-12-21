from pymongo import MongoClient
from modules import div_time_dict as dtd
import pprint
#db init
client = MongoClient()
db = client.proteins
homo = db.homo_proteom
gen_prot = db.gen_proteom_alpha
gen_prot2 = db.gen_proteom_beta

proteoms = [i for i in gen_prot.find()]
dt = dtd()
c = 1
for protein in proteoms:
    spec = protein['organism'].split(' ')[0]
    protein.pop('_id')
    if spec in dt.keys():
        protein.update({'div_time': float(dt[spec])})
    else:
        protein.update({'div_time': -1})
    gen_prot2.insert_one(protein)
    print(c)
    c+=1