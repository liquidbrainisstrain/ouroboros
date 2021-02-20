import time
import pprint
import textwrap
import json
import PySimpleGUI as sg

filename = '/Users/liquidbrain/projects/proteomics/ouroboros/data/user_data/builds/Membrane ProteinSevere acute respiratory syndrome coronavirus 2-build.json'

with open(filename, 'r') as file:
    build_data = json.loads(file.read())

mots = [{'mot': i['mot']} for i in build_data['mots']]

for i in mots:
    pos = build_data['seq'].find(i['mot'])
    i.update({'st_pos':build_data['seq'].find(i['mot']),
              'end_pos': build_data['seq'].find(i['mot']) + len(i['mot'])})

pprint.pprint(mots)

for i in range(len(build_data['mots'])):
    oth_mots = []
    for find in build_data['mots'][i]['finds']:
        oth_mots.append(find['seq'].strip('_')[int(find['motst']):int(find['motend'])])
    mots[i].update({'blocks': oth_mots})

print(build_data['seq'])
res_seq = []
stpos = 0
for block in mots:
    endpos = block['end_pos']
    res_seq.append(build_data['seq'][stpos:endpos])
    stpos = endpos
res_seq.append(build_data['seq'][endpos:])

print(res_seq)



