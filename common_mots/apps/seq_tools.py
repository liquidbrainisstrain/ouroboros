def makeblock(info=dict, size=50):
    import collections

    mot = info['mot']
    block = []
    clean_block = []
    lettweight = []

    if size > len(info['finds'][-1]['lseq']):
        print('Error - длина блока превышает длину исходной последовательности')
        return

    for i in info['finds']:
        if mot in i['lseq']:
            nstpos = i['lseq'].find(mot) - ((size - len(mot)) // 2)
            nendpos = (i['lseq'].find(mot) + len(mot)) + (size - len(mot) - ((size - len(mot)) // 2))
    motline = ((size - len(mot)) // 2) * '_' + mot + (size - len(mot) - ((size - len(mot)) // 2)) * '_'

    for prot in info['finds']:
        prot.update({'block': prot['lseq'][nstpos:nendpos]})
        # print(prot['seq'][nstpos:nendpos])

    for rown in range(size):
        c = collections.Counter()
        for coln in range(len(info['finds'])):
            c[info['finds'][coln]['block'][rown]] += 1
        lettweight.append(c)

    info.update({"block_weights":lettweight})
    return info

def clean_block(info, lettimes=10):
    for prot in info['finds']:
        line = ''
        for letterpos in range(len(info['finds'][-1]['block'])):
            if info["block_weights"][letterpos][prot['block'][letterpos]] < lettimes:
                line = line + '_'
            else:
                line = line + prot['block'][letterpos]
        # print(line)
        prot.update({'cblock':line})
    return info

def freq_check(info, pos, letter):
    out = []
    for protein in info:
        if protein[0][pos - 1] == letter.upper():
            out.append(protein)
    return out

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

def mot_finder2(seq1, seq2, motlen=9, cleaner='on'):
    fL = 0
    lL = motlen
    mots = []
    while lL <= len(seq1):
        if lL == len(seq1):
            break
        elif seq1[fL:lL] in seq2:
                mots.append(seq1[fL:lL])
                fL = lL
                lL += motlen
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
    res.append(mot)
    return res

def seq_liner(proteins=list):
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
        proteins[n].update({'lseq':seq})

    return(proteins)

def fasta_to_obj(proteom):
    from itertools import groupby
    def fasta_iter(fasta_name):
        fin = open(fasta_name, 'rb')

        faiter = (x[1] for x in groupby(fin, lambda line: str(line, 'utf-8')[0] == ">"))
        for header in faiter:
            name = str(header.__next__()[1:].strip(), 'utf-8')
            seq = "".join(str(s, 'utf-8').strip() for s in faiter.__next__())
            obj = {
                'name': ' '.join(name.split("OS=")[0].split(" ")[1:-1]),
                'id': name.split("|")[1],
                'ref': 'https://www.uniprot.org/uniprot/' + name.split("|")[1],
                'organism': name.split("OS=")[1].split('OX=')[0][0:-1],
                'seq': seq
            }
            yield obj

    fiter = fasta_iter(proteom)
    out_obj = []
    for ff in fiter:
        out_obj.append(ff)

    return out_obj

