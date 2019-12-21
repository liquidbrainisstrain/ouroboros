from pymongo import MongoClient
import pprint
from Bio import SeqIO

proteom = []
link = "https://www.uniprot.org/uniprot/"
res_list = []

#dbinit
client = MongoClient()
db = client.bioregulation
finds = db.finds

for seq_record in SeqIO.parse("/Users/liquidbrain/data/projects/khav-pept/human_proteom_rev.fasta", "fasta"):
    name = str(seq_record.description)
    seq = str(seq_record.seq)
    proteom.append([name, seq])


for protein in proteom:
    founds = {}
    ke = 0
    ed = 0
    dl = 0
    dg = 0
    aed = 0
    ked = 0
    edl = 0
    if protein[1].count("DS") > 0:
        founds.update({"DS": protein[1].count("DS")})
    if protein[1].count("DE") > 0:
        founds.update({"DE": protein[1].count("DE")})
    if protein[1].count("EW") > 0:
        founds.update({"EW": protein[1].count("EW")})
    if protein[1].count("DE") > 0:
        founds.update({"DE": protein[1].count("DE")})
    if protein[1].count("LK") > 0:
        founds.update({"LK": protein[1].count("LK")})
    if protein[1].count("ED") > 0:
        # founds.update({"ED": protein[1].count("ED")}) эта строка должна учитываться в конце
        if protein[1].count("EDP") > 0:
            edp = protein[1].count("EDP")
            if protein[1].count("AEDP") > 0:
                edp = edp - protein[1].count("AEDP")
                aed -= 1
                ed -= 1
                founds.update({"AEDP": protein[1].count("AEDP")})
            if protein[1].count("KEDP") > 0:
                edp = edp - protein[1].count("KEDP")
                ked -= 1
                ke -= 1
                ed -= 1
                founds.update({"KEDP": protein[1].count("KEDP")})
            if edp > 0:
                founds.update({"EDP": edp})
                ed -= edp
        if protein[1].count("EDR") > 0:
            edr = protein[1].count("EDR")
            if protein[1].count("AEDR") > 0:
                edr = edr - protein[1].count("AEDR")
                aed -= 1
                ed -= 1
                founds.update({"AEDR": protein[1].count("AEDR")})
            if edr > 0:
                founds.update({"EDR": edr})
                ed -= edr
        if protein[1].count("EDG") > 0:
            edg = protein[1].count("EDG")
            if protein[1].count("AEDG") > 0:
                edg = edg - protein[1].count("AEDG")
                aed -= 1
                dg -= 1
                ed -= 1
                founds.update({"AEDG": protein[1].count("AEDG")})
            if protein[1].count("KEDG") > 0:
                edg = edg - protein[1].count("KEDG")
                ked -= 1
                ke -= 1
                dg -= 1
                ed -= 1
                founds.update({"KEDG": protein[1].count("KEDG")})
            if edg > 0:
                founds.update({"EDG": edg})
                dg -= edg
                ed -= edg
        if (protein[1].count("AED") * -1) < aed:
            aed = aed + protein[1].count("AED")
            if protein[1].count("AEDL") > 0:
                aed = aed - protein[1].count("AEDL")
                dl -= 1
                ed -= 1
                edl -= 1
                founds.update({"AEDL": protein[1].count("AEDL")})
            if aed > 0:
                founds.update({"AED": aed})
                ed -= aed
        if (protein[1].count("KED") * -1) < ked:
            ked = ked + protein[1].count("KED")
            if protein[1].count("KEDW") > 0:
                ked = ked - protein[1].count("KEDW")
                ke -= 1
                ed -= 1
                founds.update({"KEDW": protein[1].count("KEDW")})
            if protein[1].count("KEDA") > 0:
                ked = ked - protein[1].count("KEDA")
                ke -= 1
                ed -= 1
                founds.update({"KEDA": protein[1].count("KEDA")})
            if ked > 0:
                founds.update({"KED": ked})
                ke -= ked
                ed -= ked
            if (protein[1].count("EDL") * -1) < edl:
                edl = edl + protein[1].count("EDL")
                founds.update({"EDL": protein[1].count("EDL")})
                dl -= 1
                ed -= 1
        if (protein[1].count("ED") + ed) > 0:
            founds.update({"ED": (protein[1].count("ED") + ed)})
    if (protein[1].count("KE") + ke) > 0:
        founds.update({"KE": (protein[1].count("KE") + ke)})
    if (protein[1].count("DL") + dl) > 0:
        founds.update({"DL": (protein[1].count("DL") + dl)})
    if (protein[1].count("DG") + dg) > 0:
        founds.update({"DG": (protein[1].count("DG") + dg)})



    suma = sum(founds.values())
    x = 0  # dipeptides
    y = 0  # tripeptides *20
    z = 0  # tetrapeptides * 400
    for key, value in founds.items():
        if len(key)==2:
            x += value
        if len(key)==3:
            y += value
        if len(key)==4:
            z += value
    M = 100 * (x + 20*y + 400*z) / len(protein[1])
    T = (2*x + 3*y + 4*z) / len(protein[1]) * 100
    export = {
         "name": " ".join(protein[0].split(" ")[1:-6]),
         "ref": "https://www.uniprot.org/uniprot/" + protein[0].split("|")[1],
         "count": suma,
         "M": round(M, 2),
         "T": round(T, 2),
         "length": len(protein[1]),
         "seq": protein[1],
         "peptides": founds
        }
    #to add peptides in main obj
    # for key, value in founds.items():
    #     export.update({key: value})

    res_list.append(export)

res_list = sorted(res_list, key=lambda x: x["T"])
res_list.reverse()
# pprint.pprint(res_list[2])
# for i in res_list:
#     finds.insert_one(i)
