import os
import sys

import PySimpleGUI as sg

from apps.block_app import block_app
from apps.find_mots_app import find_mots_app
from apps.compare_proteoms_app import compare_proteoms_app
from apps.find_prot_app import find_prot_app
from apps.aligner_app import aligner_app
from apps.info_app import main_page_info

os.environ['ROOT'] = os.path.dirname(os.path.abspath(sys.argv[0]))
# bundle_dir = os.path.dirname(os.path.abspath(__name__))
sg.theme('DarkPurple6')

builds = os.listdir(path=os.path.join(os.environ['ROOT'], "data", "user_data", 'builds'))

tab1 = [[sg.Button('Find Protein', font=('Helvetica', 16), size=(30, 1))],
           [sg.Button('Find Mots', font=('Helvetica', 16), size=(30, 1))],
           [sg.Button('Compare Proteoms', font=('Helvetica', 16), size=(30, 1))],
           [sg.Button('Align Sequences', font=('Helvetica', 16), size=(30, 1))]]

tab2 = [[sg.Combo(builds, key='-PROTEIN-', size=(29, 2), font=('Helvetica', 16), enable_events=True)],
           [sg.Button('Analyse Block', size=(30, 1), font=('Helvetica', 16), disabled=True)],
           [sg.Button('Make Build', size=(30, 1), font=('Helvetica', 16), disabled=True)]]

layout = [[sg.TabGroup([[sg.Tab('Tools', tab1, font=('Helvetica', 14)), sg.Tab('Build', tab2)]])],
                 [sg.Button('Exit'), sg.Button('Info')]]

window0 = sg.Window('OUROBOROS', layout)

while True:  # Event Loop
    event0, values0 = window0.read()
    # print(event0, values0)
    if event0 == sg.WIN_CLOSED or event0 == 'Exit':
        break
    elif event0 == 'Find Protein':
        window0.Hide()
        win = find_prot_app()
        if win == "Close":
            break
        window0.UnHide()
    elif event0 == 'Find Mots':
        window0.Hide()
        win = find_mots_app()
        if win == "Close":
            break
        window0.UnHide()
    elif event0 == '-PROTEIN-' and values0['-PROTEIN-'] != '':
        window0['Analyse Block'].Update(disabled=False)
    elif event0 == 'Analyse Block':
        window0.Hide()
        win = block_app(values0['-PROTEIN-'])
        if win == "Close":
            break
        window0.UnHide()
    elif event0 == 'Align Sequences':
        window0.Hide()
        win = aligner_app()
        if win == "Close":
            break
        window0.UnHide()
    elif event0 == 'Compare Proteoms':
        window0.Hide()
        win = compare_proteoms_app()
        if win == "Close":
            break
        window0.UnHide()
    elif event0 == 'Info':
        window0.Hide()
        main_page_info()
        window0.UnHide()

window0.Close()
