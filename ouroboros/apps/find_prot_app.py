def find_prot_app():
    import os
    import time
    from .seq_tools import fasta_to_obj
    from .info_app import find_protein_info
    import PySimpleGUI as sg


    ROOT = os.environ.get('ROOT')
    params = ['name', 'id', 'organism', 'seq']
    proteomspath = os.path.join(ROOT, "data", "proteoms")
    d_filename = f'search-file-{time.strftime("%m_%d_%Y-%H_%M")}'
    proteoms = os.listdir(path=proteomspath)
    user_dir = os.path.join(ROOT, "data", "user_data")

    sg.theme('DarkPurple6')
    layout = [[sg.Text('Proteom', size=(14, 1), font=('Helvetica', 14)), sg.Combo(proteoms, size=(60, 1), key="-PROTEOM-"), sg.FileBrowse()],
              [sg.Text('Search keyword', size=(14, 1), font=('Helvetica', 14)), sg.Input(key="-KEYWORD-", size=(45, 1)), sg.Text("Search in"),
               sg.InputOptionMenu(params, key='-SPARAM-', size=(10, 5), text_color='black', default_value=params[0])],
              [sg.Checkbox('Output to file', key='-OUTPUT-', enable_events=True, font=('Helvetica', 14))],
              [sg.Frame(layout=[
                  [sg.Text('File destination', font=('Helvetica', 14)), sg.Input(key='-FILEPATH-', default_text=user_dir), sg.FolderBrowse()],
                  [sg.Text('File name', font=('Helvetica', 14)), sg.Input(key='-FILENAME-', default_text=d_filename)]
              ], title='Save', visible=False, key='-SAVEMENU-', font=('Helvetica', 14))],
              [sg.MLine(size=(100, 12), key='-ML-', reroute_stdout=True, write_only=True, autoscroll=True, auto_refresh=True)],
              [sg.Button("Back"), sg.Button("Find", size=(70, 1), pad=(20,1)), sg.Button('Info')]]

    window = sg.Window('Find Protein in Proteom', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            return 'Close'
        elif event == 'Back':
            break
        elif event == "Info":
            window.Hide()
            find_protein_info()
            window.UnHide()
        elif event == "Find":
            del values['Browse0'], values['Browse']
            if '' not in values.values():
                if values["-PROTEOM-"] in proteoms:
                    proteom = fasta_to_obj(os.path.join(proteomspath, values["-PROTEOM-"]))
                else:
                    proteom = fasta_to_obj(values["-PROTEOM-"])

                pattern = values['-KEYWORD-']
                param = values['-SPARAM-']
                if param == 'seq':
                    pattern = pattern.upper()
                line0 = f'Search pattern: {pattern}, Search by {param} '
                line = f'Search pattern: {pattern}, Search by {param} '
                print(line0)

                if values['-OUTPUT-'] == True:
                    if values['-FILENAME-'] != d_filename and values['-FILENAME-'] != '':
                        d_filename = values['-FILENAME-']

                    if values['-FILEPATH-'] == user_dir:
                        filename = f'{user_dir}/{d_filename}.txt'
                    else:
                        filename = f'{values["-FILEPATH-"]}/{d_filename}.txt'

                    with open(filename, 'a') as file:
                        file.write(line0)
                        for protein in proteom:
                            if pattern in protein[param]:
                                if param == 'seq':
                                    line = f'{protein["name"]}\n{protein["organism"]}\nPositions:[{protein["seq"].find(pattern) + 1}-{protein["seq"].find(pattern) + 1 + len(pattern)}]\n{protein["id"]}\n{protein["seq"]}\n\n'
                                else:
                                    line = f'{protein["name"]}\n{protein["organism"]}\n{protein["id"]}\n{protein["seq"]}\n\n'
                                file.write(line)
                else:
                    for protein in proteom:
                        if pattern in protein[param]:
                            if param == 'seq':
                                line = f'{protein["name"]}\n{protein["organism"]}\nPositions:[{protein["seq"].find(pattern) + 1}-{protein["seq"].find(pattern) + 1 + len(pattern)}]\n{protein["id"]}\n{protein["seq"]}\n\n'
                            else:
                                line = f'{protein["name"]}\n{protein["organism"]}\n{protein["id"]}\n{protein["seq"]}\n\n'
                            print(line)
                    if line == line0 or line is None:
                        print('No results')
                print('Done')
            else:
                print("Some values are absent")
                print([i for i in values.keys() if values[i]==''])

        elif values['-OUTPUT-'] == True:
            window['-SAVEMENU-'].Update(visible=True)



    window.Close()








