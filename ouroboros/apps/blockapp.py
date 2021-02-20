def blockapp(protein):
    import json
    import os
    import textwrap

    import PySimpleGUI as sg

    from .seq_tools import makeblock
    from .seq_tools import clean_block
    from .seq_tools import freq_check
    from .infoapp import analyze_block_info

    ROOT = os.environ.get('ROOT')
    work_protein = os.path.join(ROOT, 'data', 'user_data', 'builds', protein)

    with open(work_protein, 'r') as file:
        work_protein = json.loads(file.read())

    # print(work_protein)

    sg.theme('DarkPurple6')

    motslist = [i['mot'] for i in work_protein['mots']]

    layout = [[sg.Frame(layout=[[sg.Text('Mot for analyze'),
                                 sg.Combo(motslist, key="-MOT-", size=(20, 5), default_value=motslist[0]),
                                 sg.Text(size=(15, 1), key="-MOTOUT-")],
                                [sg.Text('Block size'), sg.Slider(range=(10, 70),
                                                                  key="-SIZE-",
                                                                  default_value=30,
                                                                  size=(20, 15),
                                                                  orientation='horizontal',
                                                                  font=('Courier New', 14))]],
                        title='Block options', title_color='red', font=('Courier New', 15))],
              [sg.Button('Make block'), sg.Button('Info'), sg.Button('Back')],
              ]

    window = sg.Window('Choose mot for Block', layout)

    # ------------ window Event Loop--------------
    while True:
        event, values = window.read()
        # print(event, values)
        if event == sg.WIN_CLOSED:
            return 'Close'
        elif event == 'Back':
            break
        elif event == 'Info':
            window.Hide()
            analyze_block_info()
            window.UnHide()
        elif event == 'Make block':
            window["-MOTOUT-"].Update(values["-MOT-"])
            for i in work_protein['mots']:
                if i['mot'] == values["-MOT-"]:
                    info = i
            res = makeblock(info=info, size=int(values["-SIZE-"]))

            headers = ['block', 'name', 'organism', 'dT']
            weights = res['block_weights']
            out = []
            for i in range(len(weights)):
                line = ''
                for item in sorted(weights[i].items(), key=lambda pair: pair[1], reverse=True):
                    line = line + f' {item[0]} - {item[1]} '
                out.append([i + 1, line])
            data = [[i['block'], i['name'], i['organism'], i['dT']] for i in res['finds']]
            window.Hide()
            tab1_layout = [
                [sg.Text(f'Анализируемый мот {values["-MOT-"]}')],
                [sg.Table(values=data,
                          justification="left",
                          headings=headers,
                          font=('Courier New', 14),
                          num_rows=20,
                          max_col_width=50,
                          key='-OUT1-')],
                [sg.Input(key='lettimes', size=(5, 1)), sg.Text('Letter Frequency'),
                 sg.Input(key='pos', size=(5, 1)), sg.Text('Position'), sg.Input(key='lett', size=(5, 1)),
                 sg.Text('Letter'),
                 sg.Checkbox('Splitted', key='split'), sg.Button('Filter'), sg.Button('Clean')]
            ]
            tab2_layout = [[sg.Table(values=out,
                                     headings=['Position', 'Letters'],
                                     justification="left",
                                     font=('Courier New', 12),
                                     num_rows=20,
                                     max_col_width=100,
                                     key='-OUT2-')]]
            layout2 = [[sg.TabGroup([[sg.Tab('Block', tab1_layout), sg.Tab('Positions', tab2_layout)]])],
                       [sg.Button('Save'), sg.Button('Copy selected'), sg.Button('Info'), sg.Button('Back')]]
            window2 = sg.Window('Анализ блока', layout2)
            # ----------------------window2 Event Loop-----------------------------
            while True:
                event2, values2 = window2.read()
                # print(event2, values2)
                if event2 == sg.WIN_CLOSED:
                    return 'Close'
                elif event2 == 'Back':
                    window2.close()
                    window.UnHide()
                    break
                elif event2 == 'Info':
                    window2.Hide()
                    analyze_block_info()
                    window2.UnHide()
                elif event2 == 'Filter':
                    if values2['lettimes'] != '':
                        res = clean_block(res, lettimes=int(values2['lettimes']))
                        data = [[i['cblock'], i['name'], i['organism'], i['dT']] for i in res['finds']]
                    else:
                        pass

                    if values2['pos'] != '' and values2['lett'] != '':
                        data = freq_check(data, int(values2['pos']), values2['lett'].upper())
                        window2['-OUT1-'].Update(data)

                    if values2['split'] == True:
                        for protein in data:
                            line = ''
                            for seq in textwrap.wrap(protein[0], 10):
                                line = line + seq + ' '
                            protein[0] = line

                    window2['-OUT1-'].Update(data)

                if event2 == 'Clean':
                    data = [[i['block'], i['name'], i['organism'], i['dT']] for i in res['finds']]
                    window2['-OUT1-'].Update(data)

                if event2 == 'Save':
                    filename = res['mot'] + 'block.csv'
                    with open(filename, 'w') as file:
                        line = ' Block; Protein name; Organism; dT\n'
                        file.write(line)
                        for i in data:
                            line = f' {i[0]}; {i[1]}; {i[2]}; {i[3]}\n'
                            file.write(line)

                if event2 == 'Copy selected':
                    if len(values2['-OUT1-']) > 0:
                        for i in values2['-OUT1-']:
                            print(data[i])
                    else:
                        print('Copy error')

    window.close()