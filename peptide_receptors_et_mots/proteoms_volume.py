from pymongo import MongoClient
from modules import seq_liner
import time
import collections
import pprint

start_time = time.time()
#db init
client = MongoClient()
db = client.proteins
homo = db.homo_proteom
gen_prot = db.gen_proteom_alpha
receptors = db.receptors
result = db.rec_result_insulin_8

gen_proteom = [i for i in gen_prot.find()]

c = collections.Counter()

for protein in gen_proteom:
    c[protein['organism']] += 1

dt = {}
with open('/Users/liquidbrain/MEGAsync/projects/Proteomics/taxons_list.csv', 'r') as file:
    for line in file:
        line = line.strip('\n').split(',')
        # print(line)
        if line[0] not in dt.keys():
            dt.update({line[0]: line[1]})
res_list = []
for key, value in c.items():
    if key.split(' ')[0] in dt.keys():
        # print(key, value, "dt -- ", int(float(dt[key.split(' ')[0]])))
        res_list.append([key, value, int(float(dt[key.split(' ')[0]]))])
    else:
        # print(key, value, "dt -- ?")
        res_list.append([key, value, -1])

res_list = sorted(res_list, key=lambda item: item[2], reverse=True)

with open('/Users/liquidbrain/Desktop/proteoms_info.csv', 'w') as file:
    line = "Organism; Proteom volume; Div Time \n"
    file.write(line)
    for i in res_list:
        line = "{};{};{}\n".format(i[0], i[1], i[2])
        file.write(line)

# with open('/Users/liquidbrain/Desktop/res_for_proteom.csv', 'w') as file:
#     line = ' Organism ; Proteom volume\n'
#     file.write(line)
#     for key, value in c.items():
#         line = '{};{}\n'.format(key, value)
#         file.write(line)

print("--- %s seconds ----" % (time.time() - start_time))