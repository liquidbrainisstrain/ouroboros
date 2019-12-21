from pymongo import MongoClient
from modules import mot_finder
import time
start_time = time.time()

client = MongoClient()
db = client.proteins
homo = db.homo_proteom
gen_prot = db.gen_proteom_alpha
receptors = db.receptors
result = db.rec_result_insulin_8

receptors_prots = [i for i in receptors.find()]
general_proteom = []
c = 0

for protein in gen_prot.find():
    if protein['organism'] != "Homo sapiens":
        general_proteom.append(protein)

for r_protein in receptors_prots[23:24]:
    obj = {'name': r_protein['name'],
           "seq": r_protein["Sequence"],
           'mots': []}
    for g_protein in general_proteom:
        mots = mot_finder(r_protein["Sequence"], g_protein["seq"], 8)
        c += 1
        if c % 1000 == 0:
            print(c, "done")

        if len(mots) > 0:
            print("success")
            mot = {
                "mots": mots,
                "prot_info": g_protein
            }
            obj['mots'].append(mot)

    # if len(obj['mots']) > 0:
    #     result.insert_one(obj)



print("--- %s seconds ----" % (time.time() - start_time))