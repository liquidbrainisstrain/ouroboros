import os

import PySimpleGUI as sg
from pymongo import MongoClient

from apps.blockapp import blockapp
from apps.findmotsoneprotapp import findmotsoneprotapp
from apps.findmotsproteomsapp import findmotsproteomsapp
from apps.findprotapp import findprotapp

client = MongoClient()
db = client.proteins
data = db.enzymes
gen = db.gen_proteom_beta

os.environ['ROOT'] = os.path.dirname(os.path.abspath(__name__))

sg.theme('DarkPurple6')
protlist = [i['name'] for i in data.find()]

layout0 = [
    [sg.Button('Find Protein')],
    [sg.Button('Find Mots')],
    [sg.Combo(protlist, key='-PROTEIN-', size=(20, 5))],
    [sg.Button('Analyse Block', disabled=False)],
    [sg.Button('Compare Proteoms')],
    [sg.Button('Exit')]
    ]

window0 = sg.Window('Выбери прогу', layout0)

while True:  # Event Loop
    event0, values0 = window0.read()
    print(event0, values0)
    if event0 == sg.WIN_CLOSED or event0 == 'Exit':
        break
    elif event0 == 'Find Protein':
        window0.Hide()
        findprotapp()
        window0.UnHide()
    elif event0 == 'Find Mots':
        window0.Hide()
        findmotsoneprotapp()
        window0.UnHide()
    elif event0 == 'Analyse Block':
        window0.Hide()
        blockapp(values0['-PROTEIN-'])
        window0.UnHide()
    elif event0 == 'Compare Proteoms':
        window0.Hide()
        findmotsproteomsapp()
        window0.UnHide()


window0.Close()