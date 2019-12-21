from pymongo import MongoClient
import time
import collections
import pprint
start_time = time.time()

client = MongoClient()
db = client.proteins
homo = db.homo_proteom
gen_prot = db.gen_proteom_alpha
receptors = db.receptors
result = db.rec_result_insulin_8

c = collections.Counter()
# for i in list_of_names:
#     c[i] += 1
dt = {}
with open('/Users/liquidbrain/MEGAsync/projects/Proteomics/taxons_list.csv', 'r') as file:
    for line in file:
        line = line.strip('\n').split(',')
        # print(line)
        if line[0] not in dt.keys():
            dt.update({line[0]: line[1]})

res = [i for i in result.find()]

for i in res:
    for j in i['mots']:
        # if j['prot_info']['organism'] == 'Plasmodium falciparum (isolate 3D7)':
        #     print(i['name'])
        #     print(j)
        c[j['prot_info']['organism']] += 1
res_list = []
for key, value in c.items():
    if key.split(' ')[0] in dt.keys():
        # print(key, value, "dt -- ", dt[key.split(' ')[0]])
        res_list.append([key, value, float(dt[key.split(' ')[0]])])
    else:
        # print(key, value, "dt -- ?")
        res_list.append([key, value, -1])

res_list = sorted(res_list, key=lambda item: item[2], reverse=True)

with open('/Users/liquidbrain/Desktop/res_for_insulin.csv', 'w') as file:
    line = "Organism; Mots count; Div Time \n"
    file.write(line)
    for i in res_list:
        line = "{};{};{}\n".format(i[0], i[1], i[2])
        file.write(line)
        # print(i[0], i[1], i[2])



