import pprint
import time
import collections
from pymongo import MongoClient

start_time = time.time()
#db init
client = MongoClient()
db = client.proteins
homo = db.homo_proteom

proteom = [i for i in homo.find()]

khav_pept = {
 "Epitalon": "AEDG",
 "Pinealon": "EDR",
 "Chonluten": "EDG",
 "Vilon": "KE",
 "Thymogen": "EW",
 "Pancragen": "KEDW",
 "Bronchogen": "AEDL",
 "Cartalax": "AED",
 "Vesugen": "KED",
 "Crystagen": "EDP",
 "Ovagen": "EDL",
 "Prostasmax": "KEDP",
 "Livagen": "KEDA",
 "Cortagen": "AEDP",
 "Cardiogen": "AEDR",
 "Testagen": "KEDG",
 "Leucyllysine": "LK",
 "GA": "ED",
 "D2": "DW",
 "D4": "DG",
 "D5": "DL",
 "D7": "DS",
 "A8": "DE",
}

life_prots = ['Growth/differentiation factor 11', 'Fibronectin type III domain-containing protein 5', 'Metalloproteinase inhibitor 2', 'Mesencephalic astrocyte-derived neurotrophic factor',
              'Cerebral dopamine neurotrophic factor', 'Oxytocin-neurophysin 1', 'Osteocalcin', 'Fibroblast growth factor 19', 'Fibroblast growth factor 21',
              'Fibroblast growth factor 23', 'Beta-nerve growth factor', 'Brain-derived neurotrophic factor', 'Nicotinamide phosphoribosyltransferase']
death_prots = ['Eotaxin', 'Growth/differentiation factor 15', 'Beta-2-microglobulin', 'Junctional adhesion molecule A', 'Junctional adhesion molecule B', 'Junctional adhesion molecule C']


for protein in death_prots:
    for i in proteom:
        if protein == i['name']:
            c = 0
            obj = {'name': i['name']}
            for value in khav_pept.values():
                if i["Sequence"].count(value) > 0:
                    obj.update({value: i["Sequence"].count(value)})
                    c += i["Sequence"].count(value)
            obj.update({"pept_count": c})
            pprint.pprint(obj)



print("--- %s seconds ----" % (time.time() - start_time))