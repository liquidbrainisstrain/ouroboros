import xml.etree.ElementTree as ET
from pymongo import MongoClient
import pprint

client = MongoClient()
db = client.bioregulation
finds = db.human_proteom1

filename = "/Users/liquidbrain/MEGAsync/projects/Proteomics/test.xml"
# filename = "test.xml"
counter = 0
out_list = []

tree = ET.parse(filename)
root = tree.getroot()

#general build
for entry in root.findall('{http://uniprot.org/uniprot}entry'):
    for protein in entry.findall('{http://uniprot.org/uniprot}protein'):
        prot = {
            "Uniprot_ids": [],
            "location": "?"
        }
        #get name
        name = protein.find('{http://uniprot.org/uniprot}recommendedName').find('{http://uniprot.org/uniprot}fullName')
        prot.update({"name": name.text})

        #get species
        for org in entry.findall('{http://uniprot.org/uniprot}organism'):
            for name in org.findall('{http://uniprot.org/uniprot}name'):
                if name.get("type") == "scientific":
                    prot.update({"species": name.text})


        #get function
        for comment in entry.findall('{http://uniprot.org/uniprot}comment'):
            # print(comment.attrib)
            if comment.get("type") == "function":
                prot.update({"Function": comment.find('{http://uniprot.org/uniprot}text').text})

        #get uniprot ID
        for id in entry.findall('{http://uniprot.org/uniprot}accession'):
            prot["Uniprot_ids"].append(id.text)

        #get sequence
        for seq in entry.findall('{http://uniprot.org/uniprot}sequence'):
            prot.update({"Sequence": seq.text.replace('\n', '')})
            prot.update({"length": len(seq.text.replace('\n', ''))})

        #get location
        for comment in entry.findall('{http://uniprot.org/uniprot}comment'):
            try:
                if comment.get("type") == "subcellular location":
                    location = comment.find('{http://uniprot.org/uniprot}subcellularLocation').findall(
                        '{http://uniprot.org/uniprot}location')
                    if len(location) > 0:
                        line = ""
                        for i in location:
                            line = line + i.text + "/"
                    else:
                        line = "?"
                    prot.update({"location": line})
            except AttributeError:
                prot.update({"location": "?"})
        if "Function" not in prot.keys():
            prot.update({"Function":"?"})
        out_list.append(prot)
        counter+=1
        # print(counter)


for i in out_list:
    pprint.pprint(i)
    # finds.insert_one(i)
