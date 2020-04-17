from pymongo import MongoClient
import time
import collections

start_time = time.time()
#db init
client = MongoClient()
db = client.proteins
homo = db.homo_proteom
gen_prot = db.gen_proteom_alpha
receptors = db.receptors

c = collections.Counter()
# proteom = [i for i in gen_prot.find()]
homo_proteom = [i for i in homo.find()]
names = []

for protein in homo_proteom:
    if "insulin" in protein['name'].lower():
        # names.append(protein)
        # print(protein['name'])
        if "receptor" in protein['name'].lower():
            names.append(protein)
            print(protein['name'])
            # print(protein['Function'])

# for i in names:
#     receptors.insert_one(i)

print("--- %s seconds ----" % (time.time() - start_time))
