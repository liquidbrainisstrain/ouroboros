from pymongo import MongoClient
import pprint
import textwrap
import collections

#db init
client = MongoClient()
db = client.proteins
mots = db.mots_v3

mot = 'VNSVLERL'
size = int(input('Размер блока (ед) '))

def makeblock(info=dict, size=50):
    import collections

    mot = info['mot']
    block = []
    clean_block = []
    lettweight = []

    if size > len(info['finds'][-1]['seq']):
        print('Error - длина блока превышает длину исходной последовательности')
        return

    for i in info['finds']:
        if mot in i['seq']:
            nstpos = i['seq'].find(mot) - ((size - len(mot)) // 2)
            nendpos = (i['seq'].find(mot) + len(mot)) + (size - len(mot) - ((size - len(mot)) // 2))
    motline = ((size - len(mot)) // 2) * '_' + mot + (size - len(mot) - ((size - len(mot)) // 2)) * '_'

    for prot in info['finds']:
        prot.update({'block': prot['seq'][nstpos:nendpos]})
        print(prot['seq'][nstpos:nendpos])

    for rown in range(size):
        c = collections.Counter()
        for coln in range(len(info['finds'])):
            c[info['finds'][coln]['block'][rown]] += 1
        lettweight.append(c)

    info.update({"block_weights":lettweight})
    return info

#info is [0org, 1name, 2dT, 3sequence, 4block, 5clean_block]

def analyse_block(info):
    lettimes = int(input('Задай частоту буквы '))
    def split_seqs(info, blocktype='block'):
        for protein in info['finds']:
            line = ''
            for seq in textwrap.wrap(protein[blocktype], 10):
                line = line + seq + ' '
            print(line)
        return

    def clean_block(info, lettimes=10):
        for prot in info['finds']:
            line = ''
            for letterpos in range(len(info['finds'][-1]['block'])):
                if info["block_weights"][letterpos][prot['block'][letterpos]] < lettimes:
                    line = line + '_'
                else:
                    line = line + prot['block'][letterpos]
            prot.update({'cblock':line})
        return info

    def freq_check(info):
        out = []
        log = input("нужно вывести частоты по позициям?(y/n) ")
        if log == 'y':
            for i in range(len(info['block_weights'])):
                print(i + 1, info['block_weights'][i])

        pos = int(input('Введите поцицию '))
        letter = input('Введите букву ').upper()
        for protein in info['finds']:
            if protein['block'][pos - 1] == letter:
                out.append(protein)
        info['finds'] = out
        res = clean_block(info, lettimes)
        for i in info['finds']:
            print(i['cblock'])
        return res

    split_seqs(clean_block(info, lettimes), 'cblock')

    log = input('необходим частотный анализ? y/n ')
    if log == 'y':
        res = freq_check(info)
        return res
    else:
        return info


def block_output(info):
    filename = info['mot'] + 'block.csv'
    with open(filename, 'w') as file:
        line = ' Organism; dT; protein; sequence\n'
        file.write(line)
        for i in info['finds']:
            line = ' {}; {}; {}; {}\n'.format(i['organism'], i['dT'], i['name'], i['cblock'])
            file.write(line)

        # line = 'mot sequence; - ;letter power; {}'.format(motline)
        # file.write(line)


res = makeblock(info=mots.find_one({'mot':mot}), size=size)
# res = analyse_block(res)
# # pprint.pprint(res)
#
# log = input('Необходим вывод в файл? y/n ')
# if log == 'y':
#     block_output(res)


# log = input('Сохранить измененный объект в базе? y/n')
# if log == 'y':
#     mots.replace_one(mots.find_one({'mot': mot}), res)







