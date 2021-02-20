def findmotsoneprotapp():
    import os
    import json
    import time
    import PySimpleGUI as sg

    from .seq_tools import mot_finder_sequent, mot_changer, seq_liner, fasta_to_obj, add_div_time
    from .infoapp import find_mots_info


    ROOT = os.environ.get('ROOT')
    proteomspath = os.path.join(ROOT, "data", "proteoms")
    builds = os.path.join(ROOT, "data", "user_data", 'builds')
    taxons = os.path.join(ROOT, "data", "program_data", "taxons_list.csv")
    proteoms = os.listdir(path=proteomspath)

    sg.theme('DarkPurple6')
    layout = [[sg.Frame(layout=[
        [sg.Text('Protein name', size=(15, 1)), sg.Input(key='-PROTNAME-', size=(60, 1))],
        [sg.Text('Species div.time', size=(15, 1)), sg.Input(key='-DT-', size=(60, 1))],
        [sg.Text('Organism', size=(15, 1)), sg.Input(key='-ORG-', size=(60, 1))],
        [sg.Text('ID', size=(15, 1)), sg.Input(key='-ID-', size=(60, 1))],
        [sg.Text('Sequence', size=(15, 1)), sg.MLine(key='-SEQ-', enter_submits=True, size=(60, 5))]
    ], title='Protein info', title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='')],
        [sg.Text('Mot length'), sg.Spin(values=(6, 7, 8, 9, 10, 11, 12), size=(5,1), initial_value=8),
         sg.Text('Proteom'), sg.Combo(proteoms, size=(40,1), key="-PROTEOM-"), sg.FileBrowse()],
              [sg.MLine(size=(80, 12), k='-ML-', reroute_stdout=True, write_only=True, autoscroll=True,
                        auto_refresh=True)],
              [sg.Text('Proteom pass cycle', size=(20, 1)),
               sg.ProgressBar(100, size=(40, 20), orientation='h', key='-PROTEOMPROG-')],
              [sg.Text('Diffuse search', size=(20, 1)), sg.ProgressBar(100, size=(40, 20), orientation='h', key='-DIFFUSE-')],
              [sg.Button('Back'), sg.Button('Start', size=(67, 1), border_width=2), sg.Button('Info')]]

    window = sg.Window('Find mots for block and build tools', layout, finalize=True)

#EVENT LOOP MOTHER
    while True:
        event, values = window.read()
        # print(event, values)
        if event == sg.WIN_CLOSED:
            return 'Close'
        elif event == 'Back':
            break
        elif event == 'Info':
            window.Hide()
            find_mots_info()
            window.UnHide()
        elif event == 'Start':
            del values['Browse']
            if '' not in values.values():
                protein1 = {'name': values['-PROTNAME-'],
                            'id': values['-ID-'],
                            'organism': values['-ORG-'],
                            'dT': int(values['-DT-']),
                            'seq': values['-SEQ-'].upper(),
                            'mots': []}
                motlen = int(values['-MOTLEN-'])
                if values["-PROTEOM-"] in proteoms:
                    gproteom = fasta_to_obj(os.path.join(proteomspath, values["-PROTEOM-"]))
                else:
                    gproteom = fasta_to_obj(values["-PROTEOM-"])
                gproteom = add_div_time(taxons, gproteom)
                proteom_size = len(gproteom)

                st_time = time.time()
                print('Search for mots started')
                # find all mots

                c = 0
                seq1 = protein1['seq']
                mots = []
                for prot in gproteom:
                    if len(seq1) < motlen:
                        break
                    else:
                        c += 1
                        res = mot_finder_sequent(seq1, prot['seq'], motlen)
                        if len(res) > 0:
                            for i in res:
                                mots.append(i)
                                seq1 = seq1.replace(i, "_")
                        if c % 1000 == 0:
                            window['-PROTEOMPROG-'].update_bar(c, proteom_size)

                # sort mots by position in original sequence
                ps = {}
                for mot in mots:
                    ps.update({mot: protein1['seq'].find(mot)})
                mots = [i[0] for i in sorted(ps.items(), key=lambda pair: pair[1], reverse=False)]

                print(f'Found {len(mots)} actual mots')
                print(mots)
                print('Search for diffuse mots started')
                # diffusion mots search
                dif = 0
                for i in mots:
                    mot_obj = {'mot': i,
                               'finds': []}
                    gen_mots = mot_changer(i)
                    lgenmots = len(gen_mots)
                    c = 0
                    for mot in gen_mots:
                        for pr in gproteom:
                            if mot in pr['seq']:
                                obj = {'name': pr['name'],
                                       'organism': pr['organism'],
                                       'dT': pr['dT'],
                                       'seq': pr['seq'],
                                       'motst': pr['seq'].find(mot),
                                       'motend': pr['seq'].find(mot) + len(mot),
                                       'length': len(pr['seq'])}
                                mot_obj['finds'].append(obj)
                        c += 1
                        window['-PROTEOMPROG-'].update_bar(c, lgenmots)
                    mot_obj['finds'].append({
                        'name': protein1['name'],
                        'id': protein1['id'],
                        'organism': protein1['organism'],
                        'dT': protein1['dT'],
                        'seq': protein1['seq'],
                        'motst': protein1['seq'].find(i),
                        'motend': protein1['seq'].find(i) + len(i),
                        'length': len(protein1['seq'])})
                    dif += 1
                    print(dif)
                    window['-DIFFUSE-'].update_bar(dif, len(mots))
                    protein1['mots'].append(mot_obj)


                # alignment
                for mot in protein1['mots']:
                    mot['finds'] = seq_liner(mot['finds'])
                    mot['finds'] = sorted(mot['finds'], key=lambda item: item["dT"], reverse=True)

                print("--- %s seconds ----" % (time.time() - st_time))
                filename = f'{builds}/{protein1["name"]}-{protein1["organism"]}-build.json'
                with open(filename, 'w') as file:
                    file.write(json.dumps(protein1, indent=4, sort_keys=True))
    window.Close()
