from pymongo import MongoClient
from modules import seq_liner
import time

start_time = time.time()
#db init
client = MongoClient()
db = client.proteins
homo = db.homo_proteom
gen_prot = db.gen_proteom_alpha
receptors = db.receptors
result = db.rec_result_insulin_8

base = [i for i in result.find()]

#output csv
org_name = str(input('Введите название вида '))
with open('/Users/liquidbrain/Desktop/org_search.csv', 'a') as file:
    for item in base:
        line = 'Organism: {}; {} sequence\n'.format(org_name, item['name'])
        file.write(line)
        for mot in item['mots']:
            if org_name == mot['prot_info']['organism']:
                for m in mot['mots']:
                    l = [item['seq'], mot['prot_info']['seq']]
                    res = seq_liner(m, l)
                    line = '{};{}\n'.format(m, res[0])
                    file.write(line)
                    line = '{};{}\n'.format(mot['prot_info']['name'], res[1])
                    file.write(line)

print("--- %s seconds ----" % (time.time() - start_time))
