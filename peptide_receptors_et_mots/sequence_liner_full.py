from modules import seq_liner as SL
import time
from pymongo import MongoClient
import pprint

#db init
client = MongoClient()
db = client.proteins
archea_mots = db.archea_mots
arc = [i for i in archea_mots.find()]

def seq_liner_full(mot=str, seqs=list):
    new_seqs = []
    mot_seq = mot

    c = 0
    for i in range(len(seqs)):
        mot_pos1 = seqs[i].find(mot_seq)
        if mot_pos1 > c:
            c = mot_pos1

    for seq in seqs:
        mp = seq.find(mot_seq)
        new_seq = ('_' * (c - mp) + seq)
        mp = new_seq.find(mot_seq)
        new_seq = new_seq[:mp] + new_seq[mp:mp + len(mot_seq)] + new_seq[mp + len(mot_seq):]
        new_seqs.append(new_seq)

    sequence1 = new_seqs[0]
    sequence2 = new_seqs[1]
    с = 0
    gen_letters = ''
    if len(sequence1) < len(sequence2):
        for i in range(len(sequence1)):
            if sequence1[i] == sequence2[i]:
                gen_letters = gen_letters + sequence1[i]
                с+=1
            else:
                gen_letters = gen_letters + '_'
        homology = round(с / len(sequence1.strip('_')) * 100, 2)
    else:
        for i in range(len(sequence2)):
            if sequence1[i] == sequence2[i]:
                gen_letters = gen_letters + sequence1[i]
                с+=1
            else:
                gen_letters = gen_letters + '_'
        homology = round(с / len(sequence2.strip('_')) * 100, 2)
    return [sequence1, sequence2, gen_letters, homology]

start_time = time.time()
res = []
for protein in arc:
    homo_seq = protein['seq']
    for reg in protein['mots']:
        for mot in reg['mots']:
            res.append(seq_liner_full(mot, [homo_seq, reg['prot_info']['seq']]))
            # if res[3] > 20:
            #     for i in res:
            #         print(i)
            #     print('-------------------------------')

res = sorted(res, key=lambda x: x[3], reverse=True)

for i in res:
    if len(i[0].strip('_')) < 50 or len(i[1].strip('_')) < 50:
        continue
    else:
        pprint.pprint(i)
        print('----------------')

print("--- %s seconds ----" % (time.time() - start_time))
