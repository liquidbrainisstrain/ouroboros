from pymongo import MongoClient
from modules import mot_finder as mf
from modules import seq_liner_full as slf
import pprint

client = MongoClient()
db = client.proteins
homo = db.homo_proteom
gen = db.gen_proteom_beta
proteom = [i for i in gen.find()]

names = ['Measles', 'Rubella', 'Varicella Zoster Virus']

viruses_prots = []
for protein in proteom:
    for name in names:
        if name in protein['organism']:
            viruses_prots.append(protein)

proteom = [i for i in homo.find()]
total = len(proteom) * len(viruses_prots)
counter = 0
for protein in viruses_prots:
    result = []
    for pr in proteom:
        res = mf(pr['Sequence'], protein['seq'], motlen=8)
        if len(res) > 0:
            print('lucky!')
            lines = slf(res[0], [pr['Sequence'], protein['seq']])
            if lines[3] > 10:
                lines.append(pr['name'])
                lines.append(protein['name'])
                lines.append(protein['organism'])
                lines.append(protein['div_time'])
                pprint.pprint(lines)
                result.append(lines)
        counter+=1
        if counter % 1000 == 0:
            print(counter, 'of', total)
    result = sorted(result, key=lambda item: item[7], reverse=True)
    if len(result) > 0:
        filename = 'results/' + protein['name'] + ' - ' + protein['organism'] + '.txt'
        print(result)
        with open(filename, 'a') as file:
            for i in result:
                line = "organism - {}\n   divtime = {} \n   homology = {} \n   organism protein name - {}\n   virus protein " \
                       "name {}\n{}\n{}\n{}\n-------------------\n".format(i[6], i[7], i[3], i[4], i[5], i[0], i[1],
                                                                          i[2])
                file.write(line)
