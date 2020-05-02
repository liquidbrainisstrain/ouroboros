from pymongo import MongoClient

#db init
client = MongoClient()
db = client.proteins
homo = db.homo_proteom
gen = db.gen_proteom_beta
work_data = db.work_data
# proteom = [i for i in homo.find()]
gproteom = [i for i in gen.find()]
mots = db.mots_v3

#start here

#generate all mots

def mot_changer(mot):
    amac = ['G', 'P', 'A', 'V', 'L', 'I', 'M', 'C', 'F', 'Y', 'W', 'H', 'K', 'R', 'Q', 'N', 'E', 'D', 'S', 'T']
    c = 0
    res = []
    while c < len(mot):
        for i in amac:
            new_mot = mot[:c] + i + mot[c + 1:]
            if new_mot != mot:
                res.append(new_mot)
        c += 1
    return res

mot = input('type mot in uppercase ')
# mot = 'EVDAAVTPEERHL'

gen_mots = []
end_mots = []
gen_proteom_seqs = [i['seq'] for i in gproteom]

for i in mot_changer(mot):
    for j in mot_changer(i):
        gen_mots.append(j)

sel_mots = list(set(gen_mots))
print(len(sel_mots))
result = []
counter = 1

# find all possible mots in proteom

for mot in sel_mots:
    for pr in gproteom:
        if mot in pr['seq']:
            end_mots.append(mot)
    print(counter)
    counter += 1
end_mots = list(set(end_mots))
print('was found ', len(end_mots), ' actual mots')

result = []
counter = 1
for mot in end_mots:
    for pr in gproteom:
        if mot in pr['seq']:
            obj = {'name': pr['name'],
                   'ref': pr['ref'],
                   'organism': pr['organism'],
                   'div_time': pr['div_time'],
                   'seq': pr['seq'],
                   'motst': pr['seq'].find(mot),
                   'motend': pr['seq'].find(mot) + len(mot),
                   'length': len(pr['seq'])}
            result.append(obj)
    print(counter, "done")
    counter+=1


def seq_liner_pro(proteins=list, power = 0.8, seqtype ='tolerate'):
    import collections
    mmp = 0
    mlen = 0
    seqs = []

    for item in proteins:
        if item['motst'] > mmp:
            mmp = item['motst']

    for item in proteins:
        seq = item['seq']
        if item['motst'] < mmp:
            seq = (mmp - item['motst']) * "_" + seq
        if len(seq) > mlen:
            mlen = len(seq)
        seqs.append(seq)

    for n in range(len(seqs)):
        seq = seqs[n]
        if len(seqs[n]) < mlen:
            seq = seq + "_" * (mlen - len(seq))
        proteins[n]['seq'] = seq

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

    #output
    out = []
    for item in proteins:
        new_obj = {
            'name': item['name'],
            'ref': item['ref'],
            'organism': item['organism'],
            'dT': item['div_time'],
            'seq': item['seq']
        }
        out.append(new_obj)
    print(gen_seq)
    return([out, gen_seq])

power = 0.85
result = seq_liner_pro(result, power=power)
gens = result[1]
result = sorted(result[0], key=lambda item: item["dT"], reverse=True)

#result data export

#to file
filename = mot + '.csv'
with open(filename, 'w') as file:
    line = ' Organism; dT; protein; sequence\n'
    file.write(line)
    for item in result:
        line = ' {}; {}; {}; {}\n'.format(item['organism'], item['dT'], item['name'], item['seq'])
        file.write(line)

    line = 'Generated seq; {}; - letter power; {}'.format(power, gens)
    file.write(line)

#to mongo
obj = {'mot': mot,
       'finds': result,
       'common_seq': gens,
       'alt_mots': end_mots}

mots.insert_one(obj)


