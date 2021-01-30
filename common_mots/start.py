import PySimpleGUI as sg
from pymongo import MongoClient

from apps.blockapp import blockapp
from apps.findmotsoneprotapp import findmotsoneprot

client = MongoClient()
db = client.proteins
data = db.enzymes
gen = db.gen_proteom_beta


sg.theme('BluePurple')
protlist = [i['name'] for i in data.find()]


layout0 = [
        [sg.Button('Find mots')],
        [sg.Button('Analyse Block'), sg.Combo(protlist, key='-PROTEIN-', size=(20, 5))],
        [sg.Button('Exit')]
    ]

window0 = sg.Window('Выбери прогу', layout0)

while True:  # Event Loop
    event0, values0 = window0.read()
    # print(event0, values0)
    if event0 == sg.WIN_CLOSED or event0 == 'Exit':
        break
    if event0 == 'Find mots':
        window0.Hide()
        findmotsoneprot()
        window0.UnHide()
    if event0 == 'Analyse Block':
        window0.Hide()
        blockapp(values0['-PROTEIN-'])
        window0.UnHide()

window0.Close()