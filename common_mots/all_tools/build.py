import time
import pprint

import PySimpleGUI as sg

from pymongo import MongoClient
# from seq_tools import mot_finder2
# from seq_tools import mot_changer
# from seq_tools import seq_liner

#db init
client = MongoClient()
db = client.proteins
out = db.enzymes
gen = db.gen_proteom_beta
gproteom = [i for i in gen.find()]
mots = db.mots_v3


protein1 = {'name': 'Membrane Protein',
            'id': 'P0DTC5',
            'organism': 'Severe acute respiratory syndrome coronavirus 2',
            'dT': 0,
            'seq': 'MADSNGTITVEELKKLLEQWNLVIGFLFLTWICLLQFAYANRNRFLYIIKLIFLWLLWPVTLACFVLAAVYRINWITGGIAIAMACLVGLMWLSYFIASFRLFARTRSMWSFNPETNILLNVPLHGTILTRPLLESELVIGAVILRGHLRIAGHHLGRCDIKDLPKEITVATSRTLSYYKLGASQRVAGDSGFAAYSRYRIGNYKLNTDHSSSSDNIALLVQ',
            'mots': []}
motlen = 8

st_time = time.time()
#find all mots

c = 0
seq1 = protein1['seq']
mots = []
for prot in gproteom:
    if len(seq1) < motlen:
        break
    else:
        c += 1
        res = mot_finder2(seq1, prot['seq'], motlen)
        if len(res) > 0:
            for i in res:
                mots.append(i)
                seq1 = seq1.replace(i, "_")
            print(c)

#sort mots by position in original sequence
ps = {}
for mot in mots:
    ps.update({mot:protein1['seq'].find(mot)})
mots = [i[0] for i in sorted(ps.items(), key=lambda pair: pair[1], reverse=False)]

#diffusion mots search
c = 0
for i in mots:
    mot_obj = {'mot': i,
               'finds':[]}
    for mot in mot_changer(i):
        for pr in gproteom:
            if mot in pr['seq']:
                obj = {'name': pr['name'],
                       'organism': pr['organism'],
                       'dT': pr['div_time'],
                       'seq': pr['seq'],
                       'motst': pr['seq'].find(mot),
                       'motend': pr['seq'].find(mot) + len(mot),
                       'length': len(pr['seq'])}
                mot_obj['finds'].append(obj)
    mot_obj['finds'].append({
        'name': protein1['name'],
        'id': protein1['id'],
        'organism': protein1['organism'],
        'dT': protein1['dT'],
        'seq': protein1['seq'],
        'motst': protein1['seq'].find(i),
        'motend': protein1['seq'].find(i) + len(i),
        'length': len(protein1['seq'])})
    print(c, "done")
    c+=1
    protein1['mots'].append(mot_obj)

#alignment
for mot in protein1['mots']:
    mot['finds'] = seq_liner(mot['finds'])
    mot['finds'] = sorted(mot['finds'], key=lambda item: item["dT"], reverse=True)

print("--- %s seconds ----" % (time.time() - st_time))
out.insert_one(protein1)





