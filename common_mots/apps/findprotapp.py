def findprotapp():
    import os
    import time
    from .seq_tools import fasta_to_obj
    import PySimpleGUI as sg


    sg.theme('DarkPurple6')
    ROOT = os.environ.get('ROOT')
    params = ['name', 'id', 'organism', 'seq']
    proteomspath = os.path.join(ROOT, "data", "proteoms")
    proteoms = os.listdir(path=proteomspath)
    layout = [[sg.Text('Proteom', size=(12, 1)), sg.Combo(proteoms, size=(55, 1), key="-PROTEOM-"), sg.FileBrowse()],
              [sg.Text('Search keyword', size=(12, 1)), sg.Input(key="-PATTERN-", size=(40, 1)), sg.Text("Search in"),
               sg.InputOptionMenu(params, key='-SPARAM-', size=(10, 5), text_color='black', default_value=params[0])],
              [sg.MLine(size=(80, 12), key='-ML-', reroute_stdout=True, write_only=True, autoscroll=True,
                        auto_refresh=True)],
              [sg.Button("Back"), sg.Button("Find", size=(40, 1), pad=(20,1)),
               sg.Checkbox('Output to file', key='-OUTPUT-'), sg.Button('Info', pad=(20, 1))]]

    window = sg.Window('Find Protein in Proteom', layout)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Back':
            break
        if event == "Find":
            if values["-PROTEOM-"] in proteoms:
                proteom = fasta_to_obj(os.path.join(proteomspath, values["-PROTEOM-"]))
            else:
                proteom = fasta_to_obj(values["-PROTEOM-"])

            pattern = values['-PATTERN-']
            param = values['-SPARAM-']
            line0 = f'Search pattern: {pattern}, Search by {param}'
            line = f'Search pattern: {pattern}, Search by {param}'
            print(line0)
            if values['-OUTPUT-'] == True:
                outfilepath = '/Users/liquidbrain/projects/proteomics/common_mots/data/user_data/'  # нужно изменить
                filename = f'{outfilepath}search{pattern}-{str(time.ctime())}.txt'
                with open(filename, 'a') as file:
                    file.write(line0)
                    for protein in proteom:
                        if pattern in protein[param]:
                            line = f'{protein["name"]}\n {protein["organism"]}\n {protein["id"]}\n {protein["seq"]}\n\n'
                            file.write(line)
            else:
                for protein in proteom:
                    if pattern in protein[param]:
                        line = f'{protein["name"]}\n {protein["organism"]}\n {protein["id"]}\n {protein["seq"]}\n\n'
                        print(line)
                if line == line0 or line is None:
                    print('No results')
            print('Done')

    window.Close()








