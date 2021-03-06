def compare_proteoms_app():
    import os
    import time
    import pprint

    import PySimpleGUI as sg

    from .seq_tools import fasta_to_obj, mot_finder, mot_finder_sequent
    from .info_app import compare_proteoms_info

    sg.theme('DarkPurple6')
    stype = ['sequent', 'casual']
    ROOT = os.environ.get('ROOT')
    proteomspath = os.path.join(ROOT, "data", "proteoms")
    result_file_path = os.path.join(ROOT, "data", "user_data")
    proteoms = os.listdir(path=proteomspath)
    d_filename = d_filename = f'compare-file-{time.strftime("%m_%d_%Y-%H_%M")}'

    layout = [
        [sg.Text('FROM proteom path', size=(17,1), font=('Helvetica', 14)), sg.Combo(proteoms, key="-PATHFROM-", size=(40,1)), sg.FileBrowse()],
        [sg.Text('TO proteom path', size=(17,1), font=('Helvetica', 14)), sg.Combo(proteoms, key="-PATHTO-", size=(40,1)), sg.FileBrowse()],
        [sg.Text('Mot length', font=('Helvetica', 14)), sg.Spin(values=(4, 5, 6, 7, 8, 9, 10, 11, 12), key="-MOTLEN-", size=(5,1), initial_value=8),
         sg.Text("Search way", font=('Helvetica', 14)), sg.InputOptionMenu(stype, key='-STYPE-', size=(10, 5), text_color='black', default_value=stype[1])],
        [sg.Text('File name', font=('Helvetica', 14)), sg.Input(key='-FILENAME-', default_text=d_filename)],
        [sg.Text('Out file path', size=(13,1), font=('Helvetica', 14)), sg.Input(default_text=result_file_path, key='-FILEPATH-'), sg.FolderBrowse()],
        [sg.Text('Proteom pass through', font=('Helvetica', 14)), sg.ProgressBar(100, size=(34, 20), orientation='h', key='-PROTEOMPROG-')],
        [sg.Button('Back'), sg.Button('Start', size=(60,1)), sg.Button('Info')]
    ]

    window = sg.Window('Compare proteoms', layout)

    while True:  # Event Loop
        event, values = window.read()
        # print(event, values)
        if event == sg.WIN_CLOSED:
            return 'Close'
        elif event == 'Back':
            break
        elif event == 'Info':
            window.Hide()
            compare_proteoms_info()
            window.UnHide()
        elif event == 'Start':
            counter = 0

            if values["-PATHFROM-"] in proteoms:
                proteomfrom = fasta_to_obj(os.path.join(proteomspath, values["-PATHFROM-"]))
            else:
                proteomfrom = fasta_to_obj(values["-PATHFROM-"])

            if values["-PATHTO-"] in proteoms:
                proteomto = fasta_to_obj(os.path.join(proteomspath, values["-PATHTO-"]))
            else:
                proteomto = fasta_to_obj(values["-PATHTO-"])

            total = len(proteomfrom) * len(proteomto)
            # print(total)
            motlen = int(values['-MOTLEN-'])
            start_time = time.time()

            if values['-STYPE-'] == 'sequent':
                for proteinfrom in proteomfrom:
                    seq1 = proteinfrom['seq']
                    mots = []
                    for proteinto in proteomto:
                        counter += 1
                        if counter % 100 == 0:
                            window['-PROTEOMPROG-'].update_bar(counter, total)
                            # print(counter)

                        if len(seq1) < motlen:
                            break
                        else:
                            res = mot_finder_sequent(seq1, proteinto['seq'], motlen=motlen)
                            if len(res) > 0:
                                for i in res:
                                    motobj = {'mot': i,
                                          'name': proteinto["name"],
                                          'info': f'/{proteinto["organism"]}/{proteinto["id"]}',
                                          'pos_to': proteinto['seq'].find(i)}
                                    mots.append(motobj)
                                    seq1 = seq1.replace(i, "_")
                    if len(mots) > 0:
                        for mot in mots:
                            mot.update({'pos_from': proteinfrom['seq'].find(mot['mot'])})
                        mots = sorted(mots, key=lambda item: item["pos_from"], reverse=False)
                        proteinfrom.update({'mots': mots})

            else:  # casual type of search
                for proteinfrom in proteomfrom:
                    seq1 = proteinfrom['seq']
                    mots = []
                    for proteinto in proteomto:
                        counter += 1
                        if counter % 100 == 0:
                            window['-PROTEOMPROG-'].update_bar(counter, total)
                            # print(counter)
                        res = mot_finder(seq1, proteinto['seq'], motlen=motlen)
                        if len(res) > 0:
                            for i in res:
                                motobj = {'mot': i,
                                          'name': proteinto["name"],
                                          'info': f'/{proteinto["organism"]}/{proteinto["id"]}',
                                          'pos_to': proteinto['seq'].find(i)}
                                mots.append(motobj)
                    if len(mots) > 0:
                        for mot in mots:
                            mot.update({'pos_from': proteinfrom['seq'].find(mot['mot'])})
                        mots = sorted(mots, key=lambda item: item["pos_from"], reverse=False)
                        proteinfrom.update({'mots': mots})

            window['-PROTEOMPROG-'].update_bar(1, 1)
            outfilepath = values['-FILEPATH-']
            if values['-FILENAME-'] != d_filename:
                d_filename = values['-FILENAME-']

            filename = f'{outfilepath}/{d_filename}.csv'
            print("--- %s seconds ----" % (time.time() - start_time))
            with open(filename, 'a') as file:
                line = f'Proteom of {proteomfrom[0]["organism"]}; MOT - Positions/Protein name/Organism/Uniprot ID\n'
                file.write(line)
                for prot in proteomfrom:
                    if 'mots' in prot.keys():
                        line = f'{prot["name"]}; Mots count - {len(prot["mots"])} MOTs\n'
                        file.write(line)
                        for mot in prot['mots']:
                            line = f'[{mot["pos_from"] + 1}-{mot["pos_from"] + len(mot["mot"])}] ;{mot["mot"]} - {mot["name"]} {mot["pos_to"] + 1}-{mot["pos_to"] + len(mot["mot"])}/{mot["info"]}\n'
                            file.write(line)

    window.Close()












