def block_app(protein):
    import json
    import os
    import textwrap
    import pprint

    import PySimpleGUI as sg

    from .seq_tools import makeblock
    from .seq_tools import clean_block
    from .seq_tools import freq_check
    from .info_app import analyze_block_info

    ROOT = os.environ.get('ROOT')
    user_dir = os.path.join(ROOT, 'data', 'user_data')
    work_protein = os.path.join(ROOT, 'data', 'user_data', 'builds', protein)

    with open(work_protein, 'r') as file:
        work_protein = json.loads(file.read())

    # print(work_protein)

    sg.theme('DarkPurple6')

    motslist = [i['mot'] for i in work_protein['mots']]

    layout = [[sg.Frame(layout=[[sg.Text('Mot for analyze', font=('Helvetica', 14)),
                                 sg.Combo(motslist, key="-MOT-", size=(20, 5), default_value=motslist[0]),
                                 sg.Text(size=(15, 1), key="-MOTOUT-")],
                                [sg.Text('Block size', font=('Helvetica', 14)), sg.Slider(range=(10, 70),
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
                          max_col_width=30,
                          key='-OUT1-')],
                [sg.Input(key='lettimes', size=(5, 1)), sg.Text('Letter Frequency'),
                 sg.Frame(layout=[[sg.Input(key='pos', size=(5, 1)), sg.Text('Position'), sg.Input(key='lett', size=(5, 1)),
                 sg.Text('Letter')]], title='Select by letter'),
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
                       [sg.Button('Save Block'), sg.Button('Copy selected'), sg.Button('Info'), sg.Button('Back')]]
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

                if event2 == 'Save Block':
                    d_filename = f'{res["mot"]}-block'
                    layout_save = [[sg.Text('Choose destination folder and file name or use default')],
                                   [sg.Input(key='-FILEPATH-', default_text=user_dir), sg.FolderBrowse()],
                                   [sg.Input(key='-FILENAME-', default_text=d_filename)],
                                   [sg.Button("Save")]]

                    event_s, values_s = sg.Window('Save destination', layout_save).read(close=True)

                    if values_s['-FILENAME-'] != d_filename and values_s['-FILENAME-'] != '':
                        d_filename = values_s['-FILENAME-']

                    if values_s['-FILEPATH-'] == user_dir:
                        filename = f'{user_dir}/{d_filename}.csv'
                    else:
                        filename = f'{values_s["-FILEPATH-"]}/{d_filename}.csv'

                    with open(filename, 'w') as file:
                        line = ' Block; Protein name; Organism; dT\n'
                        file.write(line)
                        for i in data:
                            line = f' {i[0]}; {i[1]}; {i[2]}; {i[3]}\n'
                            file.write(line)

                if event2 == 'Copy selected':
                    if len(values2['-OUT1-']) > 0:
                        text = ''
                        for i in values2['-OUT1-']:
                            for find in res['finds']:
                                if data[i][1] == find['name'] and data[i][2] == find['organism']:
                                    text = text + f'Organism - {find["organism"]}\nProtein Name-{find["name"]}\nSequence - {find["seq"]}\nBlock - {find["block"]}\n\n'
                        layout_copy = [[sg.MLine(text, size=(80,12))],
                                   [sg.Button("Close")]]

                        window_copy = sg.Window("Copied proteins", layout_copy)
                        while True:
                            event_copy, values_copy = window_copy.read()
                            # print(event2, values2)
                            if event_copy in (sg.WIN_CLOSED,"Close"):
                                break
                        window_copy.close()
                    else:
                        print('Copy error')

    window.close()