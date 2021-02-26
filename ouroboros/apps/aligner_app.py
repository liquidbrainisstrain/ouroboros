def aligner_app():
    import os
    import sys

    import PySimpleGUI as sg

    from .info_app import align_seqs_info
    from .seq_tools import two_seqs_liner, mot_finder

    layout = [[sg.Text('Protein1 Name', size=(15,1), font=('Helvetica', 14)), sg.Input(key='-PROTNAME1-', size=(80,1))],
              [sg.Text('Protein2 Name', size=(15,1), font=('Helvetica', 14)), sg.Input(key='-PROTNAME2-', size=(80,1))],
              [sg.Text('Protein1', size=(15,1), font=('Helvetica', 14)), sg.Input(key='-PROT1-', size=(80,1))],
              [sg.Text('Protein2', size=(15,1), font=('Helvetica', 14)), sg.Input(key='-PROT2-', size=(80,1))],
              [sg.Text('Mot', size=(15,1), font=('Helvetica', 14)), sg.Input(key='-MOT-'), sg.Text('<--- Not necessary', font=('Helvetica', 14))],
              [sg.MLine(size=(100,12), reroute_stdout=True, write_only=True, autoscroll=True)],
              [sg.Button('Back'), sg.Button('Start'), sg.Button('Info')]
              ]
    window = sg.Window('Align sequences', layout)

    # event loop
    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            return "Close"
        elif event == "Back":
            break
        elif event == 'Info':
            window.Hide()
            align_seqs_info()
            window.Unhide()
        elif event == 'Start':
            prot1 = values['-PROT1-']
            prot2 = values['-PROT2-']
            protnm1 = values['-PROTNAME1-']
            protnm2 = values['-PROTNAME2-']
            mot = values['-MOT-']
            if mot != '':
                if (mot in prot1) and (mot in prot2):
                    res = two_seqs_liner(mot, [prot1, prot2])
                    [print(i) for i in res]
                else: print('mot not in the one of the proteins')
            else:
                print('empty value')
                mots = mot_finder(prot1, prot2, motlen=6)
                if len(mots)>0:
                    res = two_seqs_liner(mots[0], [prot1, prot2])
                    [print(i) for i in res]
                else: print('No similarities')


    window.close()



