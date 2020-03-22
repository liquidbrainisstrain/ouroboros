from pymongo import MongoClient
from modules import mot_finder as mf
from modules import seq_liner_full as slf
import pprint

#db init
client = MongoClient()
db = client.proteins
homo = db.homo_proteom
proteom = [i for i in homo.find()]

#ncov proteom
dt = {}
counter = 1
with open('/Users/liquidbrain/projects/Proteomics/sars-ncov-2019/sars-ncov-proteom.csv', 'r') as file:
    for line in file:
        line = line.strip('\n').split(';')
        dt.update({counter: line[0]})
        counter+=1

pprint.pprint(dt)

result = []
counter = 0
#compare
for pr in proteom:
    for key, value in dt.items():
        res = mf(pr['Sequence'], value)
        if len(res) > 0:
            print('lucky!')
            lines = slf(res[0], [pr['Sequence'], value])
            lines.append(pr['name'])
            pprint.pprint(lines)
            result.append(lines)
        counter+=1
        if counter % 1000 == 0:
            print(counter)

pprint.pprint(result)
with open('/Users/liquidbrain/projects/Proteomics/sars-ncov-2019/result.txt', 'a') as file:
    for item in result:
        for i in item:
            line = str(i)+'\n'
            file.write(line)