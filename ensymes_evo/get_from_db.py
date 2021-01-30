from pymongo import MongoClient
import pprint
from modules import seq_liner_short as sl
from modules import equal_seq_comparator as esc
import collections

#db init
client = MongoClient()
db = client.proteins
enz = db.enzymes

# in_prot = input('Введите название белка в соответсвии с названием в db ')
power = float(input('ввести мощность общей последовательности '))
in_prot = 'Membrane Protein'

finds = enz.find_one({'name': in_prot})['mots']

for i in range(len(finds)):
    print(i, finds[i]['mot'])

motnumb = int(input('Введите номер мота из списка '))
seqs = [[i['organism'], i['name'], i['dT'], i['lseq']] for i in finds[motnumb]['finds']]
res = sl(finds[motnumb]['finds'], power=power, seqtype='tolerate', letters=False)

pprint.pprint(res)

#output table configuration
log = input("Need result output? (y/n) ")
filename = finds[motnumb]['mot'] + '.csv'
if log == 'y':
    with open(filename, 'w') as file:
        line = ' Organism; dT; protein; sequence\n'
        file.write(line)
        for item in seqs:
            line = ' {}; {}; {}; {}\n'.format(item[0], item[2], item[1], item[3])
            file.write(line)

        line = 'Generated seq; {}; - letter power; {}'.format(power, res)
        file.write(line)

#two sequences compares
log = input('Do you need to compare sequences?(y/n) ')
if log == "y":
    counter = 0
    for item in seqs:
        print(counter, item[0], item[1], item[2])
        counter += 1
    while True:
        numb = input('Input sequence numbers separfted by space ').split(" ")
        seq1 = seqs[int(numb[0])][3]
        seq2 = seqs[int(numb[1])][3]
        res = esc(seq1, seq2)
        for i in res:
            print(i)
        log = input('Do you need to compare sequences?(y/n) ')
        if log != "y":
            break
        else:
            continue