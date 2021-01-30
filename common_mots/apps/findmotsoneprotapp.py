def findmotsoneprot():
    import time
    import PySimpleGUI as sg
    from pymongo import MongoClient

    from .seq_tools import mot_finder2
    from .seq_tools import mot_changer
    from .seq_tools import seq_liner

    client = MongoClient()
    db = client.proteins
    out = db.enzymes
    gen = db.gen_proteom_beta

    sg.theme('Light Brown 3')

    layout = [[sg.Text('Protein info')],
              [sg.Text('Protein name'), sg.Input(key='-PROTNAME-', size=(20, 1))],
              [sg.Text('Protein div.time'), sg.Input(key='-DT-', size=(20, 1))],
              [sg.Text('Organism'), sg.Input(key='-ORG-', size=(20, 1))],
              [sg.Text('ID'), sg.Input(key='-ID-', size=(20, 1))],
              [sg.Text('Sequence'), sg.Input(key='-SEQ-', size=(20, 1))],
              [sg.Text('Mot length'), sg.Input(key='-MOTLEN-', size=(20, 1))],
              [sg.MLine(size=(80, 12), k='-ML-', reroute_stdout=True, write_only=True, autoscroll=True,
                        auto_refresh=True)],
              [sg.Text('Proteom pass through'),
               sg.ProgressBar(100, size=(20, 20), orientation='h', key='-PROTEOMPROG-')],
              [sg.Text('Diffuse search'), sg.ProgressBar(100, size=(20, 20), orientation='h', key='-DIFFUSE-')],
              [sg.Button('Start'), sg.Button('Exit')]]

    window = sg.Window('Find mots for block and build tools', layout, finalize=True)

    while True:
        event, values = window.read()
        # print(event, values)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Start':
            if '' not in values.values():
                protein1 = {'name': values['-PROTNAME-'],
                            'id': values['-ID-'],
                            'organism': values['-ORG-'],
                            'dT': int(values['-DT-']),
                            'seq': values['-SEQ-'],
                            'mots': []}
                motlen = int(values['-MOTLEN-'])
                gproteom = [i for i in gen.find()]
                proteom_size = len(gproteom)

                st_time = time.time()
                # find all mots

                c = 0
                seq1 = protein1['seq']
                mots = []
                for prot in gproteom:
                    if len(seq1) < motlen:
                        break
                    else:
                        c += 1
                        res = mot_finder2(seq1, prot['seq'], motlen)
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
                                       'dT': pr['div_time'],
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
                out.insert_one(protein1)
    window.Close()
