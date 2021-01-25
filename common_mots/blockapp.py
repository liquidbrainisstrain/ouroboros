import PySimpleGUI as sg
from pymongo import MongoClient
import pprint
import textwrap
import collections

#db init
client = MongoClient()
db = client.proteins
mots = db.mots_v3

sg.theme('BluePurple')

def makeblock(info=dict, size=50):
    import collections

    mot = info['mot']
    block = []
    clean_block = []
    lettweight = []

    if size > len(info['finds'][-1]['seq']):
        print('Error - длина блока превышает длину исходной последовательности')
        return

    for i in info['finds']:
        if mot in i['seq']:
            nstpos = i['seq'].find(mot) - ((size - len(mot)) // 2)
            nendpos = (i['seq'].find(mot) + len(mot)) + (size - len(mot) - ((size - len(mot)) // 2))
    motline = ((size - len(mot)) // 2) * '_' + mot + (size - len(mot) - ((size - len(mot)) // 2)) * '_'

    for prot in info['finds']:
        prot.update({'block': prot['seq'][nstpos:nendpos]})
        print(prot['seq'][nstpos:nendpos])

    for rown in range(size):
        c = collections.Counter()
        for coln in range(len(info['finds'])):
            c[info['finds'][coln]['block'][rown]] += 1
        lettweight.append(c)

    info.update({"block_weights":lettweight})
    return info

def clean_block(info, lettimes=10):
    for prot in info['finds']:
        line = ''
        for letterpos in range(len(info['finds'][-1]['block'])):
            if info["block_weights"][letterpos][prot['block'][letterpos]] < lettimes:
                line = line + '_'
            else:
                line = line + prot['block'][letterpos]
        print(line)
        prot.update({'cblock':line})
    return info

def freq_check(info, pos, letter):
    out = []
    for protein in info['finds']:
        if protein['block'][pos - 1] == letter:
            out.append(protein)
    return out



motslist = [i['mot'] for i in mots.find()]

layout = [[sg.Text('Анализируемый мот'), sg.Combo(motslist, key='mot', size=(20,5)), sg.Text(size=(15,1), key='motout')],
          [sg.Text('Размер блока'), sg.Slider(range=(10,70),
                     key='size',
                     default_value=30,
                     size=(20,15),
                     orientation='horizontal',
                     font=('Helvetica', 12))],
          [sg.Button('Make block'), sg.Button('Exit')],
          ]

window = sg.Window('Работа с блоком', layout)
while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Make block':
        # Update the "output" text element to be the value of "input" element
        window['motout'].Update(values['mot'])
        res = makeblock(info=mots.find_one({'mot': values['mot']}), size=int(values['size']))

        headers = ['block', 'name', 'organism', 'dT']
        weights = res['block_weights']
        out = []
        for i in range(len(weights)):
            line = ''
            for item in sorted(weights[i].items(), key=lambda pair: pair[1], reverse=True):
                pprint.pprint(item)
                line = line + f' {item[0]} - {item[1]} '
            out.append([i+1, line])
        data = [[i['block'], i['name'], i['organism'], i['dT']] for i in res['finds']]
        window.Hide()
        tab1_layout = [
            [sg.Text(f'Анализируемый мот {values["mot"]}')],
            [sg.Table(values=data,
                      select_mode='extended',
                      justification="left",
                      headings=headers,
                      font=('Courier New', 12),
                      num_rows=20,
                      max_col_width=50,
                      key='-OUT1-')],
            [sg.Button('Clean'), sg.Input(key='lettimes', default_text=0, size=(5,1)), sg.Text('Letter Frequency'),
             sg.Button('Choose'), sg.Input(key='pos', size=(5,1)), sg.Text('Position'), sg.Input(key='lett', size=(5,1)), sg.Text('Letter'),
             sg.Checkbox('Splitted output', key='split', enable_events=True)
             ]]
        tab2_layout = [[sg.Table(values=out,
                                 headings=['Position','Letters'],
                                 justification="left",
                                 font=('Courier New', 12),
                                 num_rows=20,
                                 max_col_width=100,
                                 key='-OUT2-')]]
        layout2 = [[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout), sg.Tab('Tab 2', tab2_layout)]])],
              [sg.Button('Save'),sg.Button('Copy selected'), sg.Button('Exit')]]
        window2 = sg.Window('Анализ блока', layout2)
        while True:  # Event Loop
            event2, values2 = window2.read()
            print(event2, values2)
            if event2 is None or event2 == 'Exit':
                window2.close()
                window.UnHide()
                break

            if event2 == 'split':
                if values2['split'] == True:
                    for protein in data:
                        line = ''
                        for seq in textwrap.wrap(protein[0], 10):
                            line = line + seq + ' '
                        protein[0] = line
                    window2['-OUT1-'].Update(data)
                else:
                    data = [[i['block'], i['name'], i['organism'], i['dT']] for i in res['finds']]
                    window2['-OUT1-'].Update(data)

            if event2 == 'Clean':
                res = clean_block(res, lettimes=int(values2['lettimes']))
                data = [[i['cblock'], i['name'], i['organism'], i['dT']] for i in res['finds']]
                window2['-OUT1-'].Update(data)

            if event2 == 'Choose':
                data = [[i['cblock'], i['name'], i['organism'], i['dT']] for i in freq_check(res, int(values2['pos']),  values2['lett'].upper())]
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

# [sg.Output(size=(100, 40), font=('Courier New', 12))]