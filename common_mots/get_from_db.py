from pymongo import MongoClient
import pprint
from modules import seq_liner_short as slp

#db init
client = MongoClient()
db = client.proteins
mots = db.mots_v3
all_mots = [i for i in mots.find()]

mot = 'LADEMGLGKTVQ'
power = 0.85

for item in all_mots:
    if item['mot'] == mot:
        seqs = [[i['organism'], i['name'], i['dT'], i['seq']] for i in item['finds']]
        res = slp(item['finds'], power=power, seqtype='tolerate')

filename = mot + '.csv'
with open(filename, 'w') as file:
    line = ' Organism; dT; protein; sequence\n'
    file.write(line)
    for item in seqs:
        line = ' {}; {}; {}; {}\n'.format(item[0], item[2], item[1], item[3])
        file.write(line)

    line = 'Generated seq; {}; - letter power; {}'.format(power, res)
    file.write(line)