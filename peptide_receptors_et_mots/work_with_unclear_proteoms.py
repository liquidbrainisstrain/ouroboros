from modules import fasta_parser as fp
from modules import mot_finder as mf
from pymongo import MongoClient
import time
import collections

#db init
client = MongoClient()
db = client.proteins
proteom = db.homo_unclear
unc = db.homo_unch
archea_mots = db.archea_mots
proteins = [i for i in unc.find()]
filename = "/Users/liquidbrain/Desktop/archea_full.fasta"
result = fp(filename)
c = 0

C = collections.Counter()
unc_archean = []
for i in result:
    if i['name'] == 'Uncharacterized protein':
        unc_archean.append(i)

col = int(input('Введите номер белка (0 - 702) '))
chis = int(input('Введите количество белков для анализа '))

start_time = time.time()
for unc_protein in proteins[col:col+chis]:
    obj = {'name': 'Uncharacterized protein',
           "seq": unc_protein["seq"],
           'mots': []}
    for arc_protein in unc_archean:
        mots = mf(unc_protein["seq"], arc_protein["seq"], 10)
        c += 1
        if c % 1000 == 0:
            print(c, "done")

        if len(mots) > 0:
            print("success")
            mot = {
                "mots": mots,
                "prot_info": arc_protein
            }
            obj['mots'].append(mot)

    if len(obj['mots']) > 0:
        archea_mots.insert_one(obj)




T = (time.time() - start_time) / (len(unc_archean)*len(proteins))

print("--- %s seconds ----" % (time.time() - start_time))

print('Скорость выполнения одной операции ', T)
