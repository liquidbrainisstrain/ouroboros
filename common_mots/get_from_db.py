from pymongo import MongoClient


#db init
client = MongoClient()
db = client.proteins
mots = db.mots_v3
all_mots = [i for i in mots.find()]

#vars and funcs
def equal_seq_comparator(seq1, seq2):
    """
    Function compares two protein sequences with equal length, lined by identical zone
    Symbol _ was used for lining sequences to the same length
    Function result - generated sequence with letters on the same positions in the both sequences
    it also contains similarity percent
    """
    c = 0
    gen_letters = ''
    for i in range(len(seq1)):
        if seq1[i] == seq2[i]:
            gen_letters = gen_letters + seq1[i]
            if seq1[i] != "_":
                c+=1
        else:
            gen_letters = gen_letters + '_'
    homology = [c, len(seq1.strip('_')), len(seq2.strip('_'))]
    return seq1, seq2, gen_letters, homology

def seq_liner_short(proteins=list, power = 0.8, seqtype ='tolerate'):
    import collections

    if seqtype == 'conservative':
        gen_seq = ''
        for i in range(len(proteins[0]['seq'])):
            let = proteins[0]['seq'][i]
            for j in range(len(proteins)):
                if let != proteins[j]['seq'][i]:
                    let = '_'
                    break
            gen_seq = gen_seq + let

    if seqtype == 'tolerate':
        #возможно нужно добавить в output
        res_list = []
        for i in range(len(proteins[0]['seq'])):
            c = collections.Counter()
            for j in range(len(proteins)):
                c[proteins[j]['seq'][i]] += 1
            res_list.append(c)

        gen_seq = ''
        for i in res_list:
            if max(i.values()) / sum(i.values()) > power:
                for key, value in i.items():
                    if value == max(i.values()):
                        gen_seq = gen_seq + key
            else:
                gen_seq = gen_seq + "_"

    print(gen_seq)
    return (gen_seq)

#input from keyboard
mot = input('type mot in uppercase ')
power = float(input('type common sequence strenth from 0.51 to 0.99 '))
# mot = 'LLDVTPLTLGID'
# power = 0.99

#get sequences from db
for item in all_mots:
    if item['mot'] == mot:
        seqs = [[i['organism'], i['name'], i['dT'], i['seq']] for i in item['finds']]
        res = seq_liner_short(item['finds'], power=power, seqtype='tolerate')

#output table configuration
log = input("Need result output? (y/n) ")
filename = mot + '.csv'
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
        res = equal_seq_comparator(seq1, seq2)
        for i in res:
            print(i)
        log = input('Do you need to compare sequences?(y/n) ')
        if log != "y":
            break
        else:
            continue
