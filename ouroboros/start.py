import os

import PySimpleGUI as sg

from apps.blockapp import blockapp
from apps.findmotsoneprotapp import findmotsoneprotapp
from apps.findmotsproteomsapp import findmotsproteomsapp
from apps.findprotapp import findprotapp

os.environ['ROOT'] = os.path.dirname(os.path.abspath(__name__))

sg.theme('DarkPurple6')

builds = os.listdir(path=os.path.join(os.environ['ROOT'], "data", "user_data", 'builds'))

column1 = [[sg.Button('Find Protein', size=(30, 1))],
           [sg.Button('Find Mots', size=(30, 1))],
           [sg.Button('Compare Proteoms', size=(30, 1))]]

column2 = [[sg.Combo(builds, key='-PROTEIN-', size=(29, 2), enable_events=True)],
           [sg.Button('Analyse Block', size=(30, 1), disabled=True)],
           [sg.Button('Make Build', size=(30, 1), disabled=True)]]

layout0 = [
    [sg.Frame(layout=[[sg.Column(column1, size=(200, 90))]], title='Mots', title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags'),
     sg.Frame(layout=[[sg.Column(column2, size=(200, 90))]], title='Build', title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],
    [sg.Button('Exit'), sg.Button('Info'), sg.Text('Program made by Alex Terekhov. Version 3.5', justification='right')]
    ]

window0 = sg.Window('OUROBOROS', layout0)

while True:  # Event Loop
    event0, values0 = window0.read()
    # print(event0, values0)
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
    elif event0 == '-PROTEIN-' and values0['-PROTEIN-']!='':
        window0['Analyse Block'].Update(disabled=False)
    elif event0 == 'Analyse Block':
        window0.Hide()
        blockapp(values0['-PROTEIN-'])
        window0.UnHide()
    elif event0 == 'Compare Proteoms':
        window0.Hide()
        findmotsproteomsapp()
        window0.UnHide()
    elif event0 == 'Info':
        sg.popup_ok('Program made by Alex Terekhov. Version 3.5')



window0.Close()