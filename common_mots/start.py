import PySimpleGUI as sg
from apps.blockapp import blockapp

def commonmots():
    import PySimpleGUI as sg

    sg.theme('BluePurple')

    layout = [
        [sg.Text('Введи белок')],
        [sg.Input(key='protein', size=(5, 1))],
        [sg.Button('Submit')]
    ]

    window = sg.Window('Определение диффузного мота', layout)

    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

    window.Close()


sg.theme('BluePurple')

layout0 = [
        [sg.Button('Find mots')],
        [sg.Button('Analyse Block')],
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
        commonmots()
        window0.UnHide()
    if event0 == 'Analyse Block':
        window0.Hide()
        blockapp()
        window0.UnHide()

window0.Close()