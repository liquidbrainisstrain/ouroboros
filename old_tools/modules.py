def mot_finder(seq1, seq2, motlen = 10, cleaner='on'):
    fL = 0
    lL = motlen
    mots = []
    while lL <= len(seq1):
        if lL == len(seq1):
            break
        elif seq1[fL:lL] in seq2:
            while lL <= len(seq1):
                if seq1[fL:lL] in seq2 and lL == len(seq1):
                    # print("!Coincedence")
                    mots.append(seq1[fL:lL])
                    break
                elif seq1[fL:(lL + 1)] in seq2:
                    lL += 1
                else:
                    # print("!Coincedence")
                    mots.append(seq1[fL:lL])
                    fL = lL - motlen
                    lL += 1
                    break
        elif seq1[fL:lL] not in seq2:
            fL += 1
            lL += 1

    if cleaner == 'on':
        medium = [i for i in mots]
        # очистить от триповторов
        for i in mots:
            line = i
            first = 0
            second = 1
            third = 2
            while third < len(line):
                if line[first] == line[second] and line[first] == line[third]:
                    medium.remove(i)
                    break
                else:
                    first += 1
                    second += 1
                    third += 1

        clean = [i for i in medium]
        # удаление ди-повторов GPGP
        for i in medium:
            first = 0
            second = 2
            while second < len(i):
                if i.count(i[first:second]) > 1:
                    clean.remove(i)
                    break
                else:
                    first += 1
                    second += 1
        return clean
    return mots

def fail_cleaner(dirty):
    """Эта функция чистит список объектов от
    последовательностей с моноповторами аминокислоты (AAA),
    диповторами (GPGP) и полных дубликатов (seq1 == seq2)
    функция требует особого форматирование фходного списка
    export = {
        # "mot": protein[0],
        # "homoprot": {
        #     "name": " ".join(protein[1].split(" ")[1:-6]),
        #     "ref": "https://www.uniprot.org/uniprot/" + protein[1].split("|")[1],
        #     "length": len(protein[3]),
        #     "seq": protein[3]
        # },
        # "virusprot": {
        #     "name1": " ".join(protein[2].split(" ")[1:-6]),
        #     "ref1": "https://www.uniprot.org/uniprot/" + protein[2].split("|")[1],
        #     "length": len(protein[4]),
        #     "seq": protein[4]
        # }
    }
    """
    #init vars
    medium = [i for i in dirty]
    end_list = []
    # очистить от триповторов
    for i in dirty:
        line = i["mot"]
        first = 0
        second = 1
        third = 2
        while third < len(line):
            if line[first] == line[second] and line[first] == line[third]:
                medium.remove(i)
                break
            else:
                first += 1
                second += 1
                third += 1

    clean = [i for i in medium]
    # удаление ди-повторов GPGP
    for i in medium:
        first = 0
        second = 2
        while second < len(i["mot"]):
            if i["mot"].count(i["mot"][first:second]) > 1:
                clean.remove(i)
                break
            else:
                first += 1
                second += 1
    #удаление дубликатов
    mots = list(set([i['mot'] for i in clean]))
    for i in mots:
        for j in clean:
            if i == j["mot"]:
                end_list.append(j)
                break

    return end_list

def mot_data_categoriser(mot, file_list):
    mot_len = len(mot)
    specs = {}
    for i in file_list:
        if i[0] in specs.keys():
            loc_dic = {
                "protname": i[1],
                "length": len(i[4]),
                "mot_pos": [i[4].find(mot), (i[4].find(mot) + mot_len)],
                "seq": i[4]
            }
            specs[i[0]]["proteins"].append(loc_dic)
        else:
            specs.update({i[0]: {
                "species": i[0],
                "family_dt": i[3],
                "proteins": [
                    {
                        "protname": i[1],
                        "length": len(i[4]),
                        "mot_pos": [i[4].find(mot), (i[4].find(mot) + mot_len)],
                        "seq": i[4]
                    }
                ]}})
    return specs

def location_parser(proteom, rang100 = False):
    categ = {
        'nucleus': ['nucleus', 'nucleolus', 'perinuclear region', 'nucleus speckle', 'nucleoplasm', 'chromosome',
                    'nucleus membrane', 'nucleus matrix',
                    'nuclear pore complex', 'nucleus inner membrane', 'nucleus envelope', 'nucleus outer membrane',
                    'perikaryon'],
        'cytoplasm': ['cytoplasm', 'cytoskeleton', 'cytosol', 'microtubule organizing center', 'centrosome',
                      'cilium axoneme', 'basement membrane',
                      'centriole'],
        'membrane': ['membrane', 'cell membrane', 'cell junction', 'postsynaptic cell membrane', 'endomembrane system',
                     'tight junction', 'basolateral cell membrane'],
        'mitochondrion': ['mitochondrion', 'mitochondrion inner membrane', 'mitochondrion outer membrane',
                          'mitochondrion matrix', 'mitochondrion membrane',
                          'mitochondrion intermembrane space'],
        'extracell': ["secreted", 'extracellular space', 'extracellular matrix']
    }
    out = []
    #range counter
    if rang100 == False:
        a = [i * 1000 for i in range(16)]
        b = [i * 1000 for i in range(1, 17)]
        rang = "rang1000"
    else:
        a = [i * 100 for i in range(166)]
        b = [i * 100 for i in range(1, 167)]
        rang = "rang100"
    #parse proteom
    check = 0
    for i in range(len(a)):
        mean_c = 0
        mean_t = 0
        counter = {
            "nucleus": 0,
            "cytoplasm": 0,
            "membrane": 0,
            "extracellular": 0,
            "mitochondrion": 0,
            "other": 0
        }
        for prot in proteom[a[i]:b[i]]:
            # print(prot['location'].split('/'))
            # print(prot['location'].split('/')[0])
            if prot['location'].split('/')[0] in categ["nucleus"]:
                counter["nucleus"] += 1
            elif prot['location'].split('/')[0] in categ["cytoplasm"]:
                counter["cytoplasm"] += 1
            elif prot['location'].split('/')[0] in categ["membrane"]:
                counter["membrane"] += 1
            elif prot['location'].split('/')[0] in categ["mitochondrion"]:
                counter["mitochondrion"] += 1
            elif prot['location'].split('/')[0] in categ["extracell"]:
                counter["extracellular"] += 1
            else:
                counter["other"] += 1
            mean_c += prot["c_dip"]
            mean_t += prot["t_dip"]

        if rang == "rang1000":
            mt = mean_t/1000
            mc = mean_c / 1000
        else:
            mt = mean_t / 100
            mc = mean_c / 100
        check += sum(counter.values())
        counter.update({rang: check, "mean_t": mt, "mean_c": mc})
        out.append(counter)
    print("Проведен анализ для пептида по рангу ", rang)
    return out

def fasta_parser(proteom_file):
    from Bio import SeqIO
    proteom = []
    result = []
    for seq_record in SeqIO.parse(proteom_file, "fasta"):
        name = str(seq_record.description)
        seq = str(seq_record.seq)
        proteom.append([name, seq])

    for prot in proteom:
        obj = {
            'name': ' '.join(prot[0].split("OS=")[0].split(" ")[1:-1]),
            'id': prot[0].split("|")[1],
            'ref': 'https://www.uniprot.org/uniprot/' + prot[0].split("|")[1],
            'organism': prot[0].split("OS=")[1].split('OX=')[0][0:-1],
            'seq': prot[1]
        }
        result.append(obj)

    return result

def seq_liner(mot=str, seqs=list):
    """This function takes mot and list of seqs,
     which contains this mot, The function returns list
    """
    # vars
    new_seqs = []
    space = "_"
    div = '-'
    mot_seq = mot

    # interacting with seqs
    c = 0
    for i in range(len(seqs)):
        mot_pos1 = seqs[i].find(mot_seq)
        if mot_pos1 > c:
            c = mot_pos1

    for seq in seqs:
        mp = seq.find(mot_seq)
        new_seq = (space * (c - mp) + seq)
        mp = new_seq.find(mot_seq)
        new_seq = new_seq[:mp] + "-" + new_seq[mp:mp+len(mot_seq)] + "-" + new_seq[mp+len(mot_seq):]
        new_seqs.append(new_seq)

    return new_seqs

def div_time_dict(filename="std"):
    dt = {}
    if filename == 'std':
        filename = '/Users/liquidbrain/MEGAsync/projects/Proteomics/taxons_list.csv'
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip('\n').split(',')
            # print(line)
            if line[0] not in dt.keys():
                dt.update({line[0]: line[1]})

    return dt

def seq_liner_full(mot=str, seqs=list):
    new_seqs = []
    mot_seq = mot

    c = 0
    for i in range(len(seqs)):
        mot_pos1 = seqs[i].find(mot_seq)
        if mot_pos1 > c:
            c = mot_pos1

    for seq in seqs:
        mp = seq.find(mot_seq)
        new_seq = ('_' * (c - mp) + seq)
        # mp = new_seq.find(mot_seq)
        # new_seq = new_seq[:mp] + new_seq[mp:mp + len(mot_seq)] + new_seq[mp + len(mot_seq):]
        new_seqs.append(new_seq)

    sequence1 = new_seqs[0]
    sequence2 = new_seqs[1]
    с = 0
    gen_letters = ''
    if len(sequence1) < len(sequence2):
        for i in range(len(sequence1)):
            if sequence1[i] == sequence2[i]:
                gen_letters = gen_letters + sequence1[i]
                с+=1
            else:
                gen_letters = gen_letters + '_'
        homology = round(с / len(sequence1.strip('_')) * 100, 2)
    else:
        for i in range(len(sequence2)):
            if sequence1[i] == sequence2[i]:
                gen_letters = gen_letters + sequence1[i]
                с+=1
            else:
                gen_letters = gen_letters + '_'
        homology = round(с / len(sequence2.strip('_')) * 100, 2)
    return [sequence1, sequence2, gen_letters, homology]

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

def dif_seq_liner(seq1,mot1,seq2,mot2):
    if seq1.find(mot1) > seq2.find(mot2):
        seq2 = '_' * (seq1.find(mot1) - seq2.find(mot2)) + seq2
    else:
        seq1 = '_' * (seq2.find(mot2) - seq1.find(mot1)) + seq1

    с = 0
    gen_letters = ''
    if len(seq1) < len(seq2):
        for i in range(len(seq1)):
            if seq1[i] == seq2[i]:
                gen_letters = gen_letters + seq1[i]
                с+=1
            else:
                gen_letters = gen_letters + '_'
        homology = round(с / len(seq1.strip('_')) * 100, 2)
    else:
        for i in range(len(seq2)):
            if seq1[i] == seq2[i]:
                gen_letters = gen_letters + seq1[i]
                с+=1
            else:
                gen_letters = gen_letters + '_'
        homology = round(с / len(seq2.strip('_')) * 100, 2)
    return [seq1, seq2, gen_letters, homology]

def seq_liner_short(proteins=list, power = 0.8, seqtype ='tolerate', letters = False):
    """
    This function generates common sequence for list of aligned proteins
    :param proteins: A list of aligned proteins. An anchor for alignment is 'mot', it is a short, less or more
     conservative fragment for all sequences. All sequences was aligned by this mot. Symbol _ was used for
    positioning one sequence under the another in one table or matrix
    :param power: Percentage value for letter in this position which is a column in the matrix of sequences
    :param seqtype: option 'conservative' is for power = 100% if less use option 'tolerate'
    :param letters: use True, if you need percentage value for each letter
    :return:Common sequence as string and letters value for each position of common sequence if letters = Tru
    as Counter obj
    """

    import collections

    if seqtype == 'conservative':
        gen_seq = ''
        for i in range(len(proteins[0]['lseq'])):
            let = proteins[0]['lseq'][i]
            for j in range(len(proteins)):
                if let != proteins[j]['lseq'][i]:
                    let = '_'
                    break
            gen_seq = gen_seq + let

    if seqtype == 'tolerate':
        #возможно нужно добавить в output
        res_list = []
        for i in range(len(proteins[0]['lseq'])):
            c = collections.Counter()
            for j in range(len(proteins)):
                c[proteins[j]['lseq'][i]] += 1
            res_list.append(c)

        gen_seq = ''
        for i in res_list:
            if max(i.values()) / sum(i.values()) > power:
                for key, value in i.items():
                    if value == max(i.values()):
                        gen_seq = gen_seq + key
            else:
                gen_seq = gen_seq + "_"

    if letters == True:
        return (gen_seq, res_list)
    else: return (gen_seq)

def seq_liner_large(proteins=list, power = 0.8, seqtype ='tolerate'):
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
    # print(gen_seq)
    return([out, gen_seq])

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

#block
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

def analyse_block(info):
    lettimes = int(input('Задай частоту буквы '))
    def split_seqs(info, blocktype='block'):
        import textwrap
        for protein in info['finds']:
            line = ''
            for seq in textwrap.wrap(protein[blocktype], 10):
                line = line + seq + ' '
            protein.update({'splblock':line})
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

    def freq_check(info, pos, letter):
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