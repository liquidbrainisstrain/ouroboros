from modules import seq_liner as SL
from modules import mot_finder
from modules import seq_liner_full as slf
from modules import mot_changer as mch
import time
from pymongo import MongoClient
import pprint

#db init
client = MongoClient()
db = client.proteins
all_proteins = db.gen_proteom_beta
arc_mots = db.archea_mots
proteoms = [i for i in all_proteins.find()]

line = 'Y_L_N_L_Y_A___L_AA___V__QLKILTTALFSV__L_RS_S___W__L_LL__G___V_A______G'
c = 0
#извлечение мотов архей
lst = []
arc_prots_and_mots = []
for item in arc_mots.find():
    if item['mots'][0]['mots'][0] not in lst:
        lst.append(item['mots'][0]['mots'][0])
        arc_prots_and_mots.append(item['mots'][0])

# pprint.pprint(arc_prots_and_mots)

#export pattern
div = '-------------------------------------------------------------\n'
c = 1
for item in arc_prots_and_mots:
    mot = item['mots'][0]
    seq = item['prot_info']['seq']
    filename = '/Users/liquidbrain/Desktop/results/' + mot + '.txt'
    with open(filename, 'w') as file:
        line = 'Result file fo mot{' + mot + '}\n'
        file.write(line)
        line = seq + '\n'
        file.write(line)
        for prot in proteoms:
            if prot['seq'].count(mot) > 0:
                res = slf(mot, [seq, prot['seq']])
                line = 'Organism - {}\n Div time - {}\n Protein - {}\n Link - {}\n Similarity percent - {}\n{}\n{}\n{}\n'.format(
                    prot['organism'], prot['div_time'], prot['name'], prot['ref'], res[3], res[0], res[1], res[2]
                )
                file.write(line)
                file.write(div)
        print(c, 'of', len(arc_prots_and_mots), 'done')
        c+=1








# result = slf(i, [seq1, protein['seq']])
# print(protein['name'], 'from organism', protein['organism'], 'has homology percent', result[3])