from pymongo import MongoClient
import pprint

#db init
client = MongoClient()
db = client.proteins
gen_prot2 = db.gen_proteom_beta
homo = db.homo_proteom

proteoms = [i for i in gen_prot2.find()]

bam = 'GSNKGAIIGLM'

#prog start

for protein in proteoms:
    if protein['seq'].count(bam) > 0:
        pprint.pprint(protein)