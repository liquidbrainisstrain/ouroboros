def blockapp(protein):
    import textwrap

    import PySimpleGUI as sg
    from pymongo import MongoClient

    from .seq_tools import makeblock
    from .seq_tools import clean_block
    from .seq_tools import freq_check

    # db init
    client = MongoClient()
    db = client.proteins
    data = db.enzymes
    work_protein = data.find_one({'name':protein})

    sg.theme('BluePurple')

    motslist = [i['mot'] for i in work_protein['mots']]

    layout = [[sg.Text('Анализируемый мот'), sg.Combo(motslist, key='mot', size=(20, 5)),
               sg.Text(size=(15, 1), key='motout')],
              [sg.Text('Размер блока'), sg.Slider(range=(10, 70),
                                                  key='size',
                                                  default_value=30,
                                                  size=(20, 15),
                                                  orientation='horizontal',
                                                  font=('Helvetica', 12))],
              [sg.Button('Make block'), sg.Button('Exit')],
              ]

    window = sg.Window('Работа с блоком', layout)

    # ------------ window Event Loop--------------
    while True:
        event, values = window.read()
        # print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Make block':
            window['motout'].Update(values['mot'])
            for i in work_protein['mots']:
                if i['mot']==values['mot']:
                    info = i
            res = makeblock(info=info, size=int(values['size']))

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
                [sg.Text(f'Анализируемый мот {values["mot"]}')],
                [sg.Table(values=data,
                          justification="left",
                          headings=headers,
                          font=('Courier New', 12),
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
            layout2 = [[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout), sg.Tab('Tab 2', tab2_layout)]])],
                       [sg.Button('Save'), sg.Button('Copy selected'), sg.Button('Exit')]]
            window2 = sg.Window('Анализ блока', layout2)
            # ----------------------window2 Event Loop-----------------------------
            while True:
                event2, values2 = window2.read()
                # print(event2, values2)
                if event2 is None or event2 == 'Exit':
                    window2.close()
                    window.UnHide()
                    break

                if event2 == 'Filter':
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