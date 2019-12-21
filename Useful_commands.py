from pymongo import MongoClient
from Bio import SeqIO
import pprint
import time
import collections

start_time = time.time()
#db init
client = MongoClient()
db = client.proteins
db2 = client.bioregulation
homo = db2.human_proteom
mots = db.all_mots_v2
info = db.all_mots_info

c = collections.Counter()
# for i in list_of_names:
#     c[i] += 1

# l = sorted(l, key=lambda item: item["count"], reverse=True)
# line = '\n {} ;{}; {}; {}\n'.format(mot['mot'], mot['org_prot'],mot['org_ref'],mot['org_seq'])

seq1 = 'MELRMIKDEWELENIRKAGKIAVNGMRIAEGEIRPGKTELEVASEVVRSSCLTGARSQKFTSPQRQRPMLSPSKMLGLGREALYPLS'
seq2 = 'EVVRSSCLTHGTYRHJOPRKAGKIAVNGMRIAEGEIRPGKTHDJJPEROGDSPQRQRPMLSPSKMLGLGREA'
print("--- %s seconds ----" % (time.time() - start_time))