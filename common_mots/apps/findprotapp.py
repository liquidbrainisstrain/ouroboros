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
    layout = [[sg.Text('Proteom'), sg.Combo(proteoms, key="-PROTEOM-"), sg.FileBrowse()],
              [sg.Text('Search keyword'), sg.Input(key="-PATTERN-", size=(40, 5))],
              [sg.Button("Find in"), sg.Combo(params, key='-SPARAM-', size=(40, 5), default_value=params[0]),
               sg.Checkbox('Output to file', key='-OUTPUT-')],
              [sg.MLine(size=(80, 12), key='-ML-', reroute_stdout=True, write_only=True, autoscroll=True,
                        auto_refresh=True)],
              [sg.Button("Exit")]]

    window = sg.Window('Find Protein in Proteom', layout)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == "Find in":
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








