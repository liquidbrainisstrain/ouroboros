from pymongo import MongoClient
import pprint
from modules import seq_liner_short as sl
import collections

#db init
client = MongoClient()
db = client.proteins
enz = db.enzymes


protein = enz.find_one({'name': "APP"})

mot = 'QKLEFSAEDV'

for i in protein['mots']:
    if i['mot'] == mot:
        s_obj = i

# res = [i['seq'] for i in s_obj['finds']]

result = sl(s_obj['finds'], power = 0.6, letters=True)
line1 = ''
line3 = ''
for i in range(len(result[0])):
    line1 = line1 + result[0][i] + ';'
    line2 = ''
    for j in result[1][i]:
        value = result[1][i][j]
        line2 = line2 + j + '-' + str(result[1][i][j]) + ' '
    line3 = line3 + line2[:-1] + ';'

print(len(line1.split(';')[:-1]))
top = ''
for i in range(1,len(line1.split(';')[:-1])+1):
    top = top + 'aa' + str(i) + ';'

print(top)
# top = 'am/ac numb;'+ top[:-1] + '\n'
# line1 = 'common;' + line1[:-1] + '\n'
# line3 = 'variants;'+ line3[:-1] + '\n'
top = top[:-1] + '\n'
line1 = line1[:-1] + '\n'
line3 = line3[:-1] + '\n'

with open('result.csv', 'w') as file:
    file.write(top)
    file.write(line1)
    file.write(line3)