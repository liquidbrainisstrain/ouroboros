def findmotsproteomsapp():
    import os
    import time
    import pprint

    import PySimpleGUI as sg

    from .seq_tools import fasta_to_obj, mot_finder, mot_finder_sequent

    sg.theme('DarkPurple6')
    stype = ['sequent', 'casual']
    ROOT = os.environ.get('ROOT')
    proteomspath = os.path.join(ROOT, "data", "proteoms")
    proteoms = os.listdir(path=proteomspath)

    layout = [
        [sg.Text('FROM proteom path', size=(17,1)), sg.Combo(proteoms, key="-PATHFROM-", size=(40,1)), sg.FileBrowse()],
        [sg.Text('TO proteom path', size=(17,1)), sg.Combo(proteoms, key="-PATHTO-", size=(40,1)), sg.FileBrowse()],
        [sg.Text('Mot length'), sg.Spin(values=(6, 7, 8, 9, 10, 11, 12), size=(5,1), initial_value=8),
         sg.Text("Search way"), sg.InputOptionMenu(stype, key='-STYPE-', size=(10, 5), text_color='black')],
        [sg.Text("Press GO to start, don't worry, it may take a while")],
        [sg.Text('Proteom pass through'), sg.ProgressBar(100, size=(34, 20), orientation='h', key='-PROTEOMPROG-')],
        [sg.Button('Back'), sg.Button('Start'), sg.Button('Info')]
    ]

    window = sg.Window('Compare proteoms', layout)

    while True:  # Event Loop
        event, values = window.read()
        # print(event, values)
        if event == sg.WIN_CLOSED or event == 'Back':
            break
        if event == 'Start':
            counter = 0
            proteomfrom = fasta_to_obj(values["-PATHFROM-"])
            proteomto = fasta_to_obj(values["-PATHTO-"])
            total = len(proteomfrom) * len(proteomto)
            # print(total)
            motlen = int(values['-MOTLEN-'])
            start_time = time.time()
            for proteinfrom in proteomfrom:
                seq1 = proteinfrom['seq']
                mots = []
                if values['-STYPE-'] == 'sequent':
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
                                              'protein': f'{proteinto["name"]}/{proteinto["organism"]}/{proteinto["id"]}'}
                                    mots.append(motobj)
                                    seq1 = seq1.replace(i, "_")
                else: #casual type if search
                    for proteinto in proteomto:
                        counter += 1
                        if counter % 100 == 0:
                            window['-PROTEOMPROG-'].update_bar(counter, total)
                            # print(counter)

                        if len(seq1) < motlen:
                            break
                        else:
                            res = mot_finder(seq1, proteinto['seq'], motlen=motlen)
                            if len(res) > 0:
                                for i in res:
                                    motobj = {'mot': i,
                                              'protein': f'{proteinto["name"]}/{proteinto["organism"]}/{proteinto["id"]}'}
                                    mots.append(motobj)


                if len(mots) > 0:
                    for mot in mots:
                        mot.update({'pos': proteinfrom['seq'].find(mot['mot'])})
                    mots = sorted(mots, key=lambda item: item["pos"], reverse=False)
                    proteinfrom.update({'mots': mots})

            pprint.pprint(proteomfrom)
            window['-PROTEOMPROG-'].update_bar(1, 1)
            outfilepath = '/Users/liquidbrain/projects/proteomics/common_mots/data/user_data/' #нужно изменить
            filename = f'{outfilepath}{str(proteomfrom[0]["organism"])}{motlen}{str(proteomto[0]["organism"])}.csv'
            print("--- %s seconds ----" % (time.time() - start_time))
            with open(filename, 'a') as file:
                line = f'Proteom of {proteomfrom[0]["organism"]}; MOT - Protein name/Organism/Uniprot ID\n'
                file.write(line)
                for prot in proteomfrom:
                    if 'mots' in prot.keys():
                        line = f'{prot["name"]}; MOTs\n'
                        file.write(line)
                        for mot in prot['mots']:
                            line = f' ;{mot["mot"]} - {mot["protein"]}\n'
                            file.write(line)

    window.Close()












