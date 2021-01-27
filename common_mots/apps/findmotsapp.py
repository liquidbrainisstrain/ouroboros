import PySimpleGUI as sg
from pymongo import MongoClient

#db init
client = MongoClient()
db = client.proteins
homo = db.homo_proteom
gen = db.gen_proteom_beta
# proteom = [i for i in homo.find()]
gproteom = [i for i in gen.find()]
mots = db.mots_v3


