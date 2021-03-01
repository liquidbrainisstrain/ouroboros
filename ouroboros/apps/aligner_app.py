def aligner_app():
    import os
    import time

    import PySimpleGUI as sg

    from .info_app import align_seqs_info
    from .seq_tools import two_seqs_liner, mot_finder

    ROOT = os.environ.get('ROOT')
    user_dir = os.path.join(ROOT, "data", "user_data")
    d_filename = f'alignment-file-{time.strftime("%m:%d:%Y-%H:%M")}'


    layout = [[sg.Text('Protein1 Name', size=(15,1), font=('Helvetica', 14)), sg.Input(key='-PROTNAME1-', size=(80,1))],
              [sg.Text('Protein1', size=(15, 1), font=('Helvetica', 14)), sg.Input(key='-PROT1-', size=(80, 1))],
              [sg.Text('Protein2 Name', size=(15,1), font=('Helvetica', 14)), sg.Input(key='-PROTNAME2-', size=(80,1))],
              [sg.Text('Protein2', size=(15,1), font=('Helvetica', 14)), sg.Input(key='-PROT2-', size=(80,1))],
              [sg.Checkbox('Output to file', key='-OUTPUT-', enable_events=True, font=('Helvetica', 14))],
              [sg.Frame(layout=[
                  [sg.Text('File destination', font=('Helvetica', 14)),
                   sg.Input(key='-FILEPATH-', default_text=user_dir), sg.FolderBrowse()],
                  [sg.Text('File name', font=('Helvetica', 14)), sg.Input(key='-FILENAME-', default_text=d_filename)]
              ], title='Save', visible=False, key='-SAVEMENU-', font=('Helvetica', 14))],
              [sg.MLine(size=(100,12), reroute_stdout=True, write_only=True, autoscroll=True)],
              [sg.Button('Back'), sg.Button('Start'), sg.Button('Info')]
              ]
    window = sg.Window('Align sequences', layout)

    # event loop
    while True:
        event, values = window.read()
        # print(event, values)
        if event == sg.WIN_CLOSED:
            return "Close"
        elif event == "Back":
            break
        elif event == 'Info':
            window.Hide()
            align_seqs_info()
            window.UnHide()
        elif event == 'Start':
            del values['Browse']
            if '' not in values.values():
                prot1 = values['-PROT1-'].upper()
                prot2 = values['-PROT2-'].upper()
                protnm1 = values['-PROTNAME1-']
                protnm2 = values['-PROTNAME2-']
                mots = mot_finder(prot1, prot2, motlen=6)
                if len(mots) > 0:
                    res = two_seqs_liner(mots[0], [prot1, prot2])
                    line = f'Protein 1 - {protnm1}\nProtein 2 - {protnm2}\n{res[0]}\n{res[1]}\n{res[2]}\nHomology - {res[3]}\n\n'
                    if values['-OUTPUT-'] == True:
                        if values['-FILENAME-'] != d_filename and values['-FILENAME-'] != '':
                            d_filename = values['-FILENAME-']

                        if values['-FILEPATH-'] == user_dir:
                            filename = f'{user_dir}/{d_filename}.txt'
                        else:
                            filename = f'{values["-FILEPATH-"]}/{d_filename}.txt'

                        with open(filename, 'a') as file:
                            file.write(line)
                            print('File output saved')
                            print(line)
                    else:
                        print('No file output')
                        print(line)
                else:
                    print('No similarities')

        elif values['-OUTPUT-'] == True:
            window['-SAVEMENU-'].Update(visible=True)


    window.close()



