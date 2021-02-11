import os
import pprint

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

def add_div_time(filename, new_proteom):
    dt = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip('\n').split(',')
            # print(line)
            if line[0] not in dt.keys():
                dt.update({line[0]: line[1]})

    for protein in new_proteom:
        spec = protein['organism'].split(' ')[0]
        if spec in dt.keys():
            protein.update({'dT': float(dt[spec])})
        else:
            protein.update({'dT': -1})
    return new_proteom

taxons = '/Users/liquidbrain/projects/proteomics/common_mots/data/program_data/taxons_list.csv'

res = fasta_to_obj('/Users/liquidbrain/projects/proteomics/common_mots/data/proteoms/all.fasta')

res = add_div_time(taxons, res)

pprint.pprint(res)


