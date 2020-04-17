from pymongo import MongoClient
from modules import mot_finder as mf
from modules import fasta_parser as fp

#db init
client = MongoClient()
db = client.proteins
homo = db.homo_proteom
gen = db.gen_proteom_beta


covid_prots = fp('/Users/liquidbrain/projects/Proteomics/sars-ncov-2019/covid-19.fasta')

prot = 'SNAADPEVCCFITKILCAHGGRMALDALLQEIALSEPQLCEVLQVAGPDRFVVLETGGEAGITRSVVATTRARVCRRKYCQRPCDNLHLCKLNLLGRCNYSQSERNLCKYSHEVLSEENFKVLKNHELSGLNKEELAVLLLQSDPFFMPEICKSYKGEGRQQICNQQPPCSRLHICDHFTRGNCRFPNCLRSHNLMDRKVLAIMREHGLNPDVVQNIQDICNSKHMQKN'

for pr in covid_prots:
    res = mf(prot, pr['seq'], motlen=7)
    if len(res) > 0:
        print(res)