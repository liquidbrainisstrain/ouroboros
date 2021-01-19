from pymongo import MongoClient
from modules import mot_finder as mf
import pprint


client = MongoClient()
db = client.proteins
homo = db.homo_proteom
gen_prot = db.gen_proteom_beta
hprots = [i for i in homo.find()]
# gprots = [i for i in gen_prot.find()]

prots = ["SEDVYANTQLVLQRP", "IMLLYPDHPTLLSYR"]

for prot in prots:
    for hprot in hprots:
        res = mf(prot, hprot["Sequence"], motlen=7)
        if len(res) > 0:
            print(res)
            print(hprot)