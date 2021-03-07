def main_page_info():
    import PySimpleGUI as sg
    info0_text = {'main': "OUROBOROS is a tool for complex analysis of protein sequences, current version 0.7. Made by Alexander Terekhov",
                  'tools': {
                      'find_prot': {'toolname': 'Find Protein',
                                    'toolinfo': 'Complex search tool for any FASTA proteom. You may choose search parameter (protein name, organism, id, sequence)'},
                      'comp_prot': {'toolname': 'Compare Proteoms',
                                    'toolinfo': "An instrument for search of short peptides called Mot's - same region in two or more different sequences"},
                      'find_mots': {'toolname': 'Find Mots',
                                    'toolinfo': 'This tool is useful for searching of mots of one protein in any proteom. Results will be used for Build and Block tools'},
                      'align': {'toolname': 'Align Sequences',
                                'toolinfo': 'It is simple allingment tool allows you to aling two or more sequences by mot'},
                      'block': {'toolname': 'Analyze Block',
                                'toolinfo': 'Block tool allows you to choose region around mot in a group of proteins aligned by mot'},
                      'build': {'toolname': 'Build',
                                'toolinfo': 'Work with this tool is in progress'}
                  }}

    info0_text_rus = {'main': "OUROBOROS - приложение для сравнения первичных последовательностей белков, текущая версия 0.7. Автор Александр Терехов",
                  'tools': {
                      'find_prot': {'toolname': 'Find Protein',
                                    'toolinfo': 'Этот инструмент позволяет найти в любом протеоме FASTA белок по запросу (protein name, organism, id, sequence)'},
                      'comp_prot': {'toolname': 'Compare Proteoms',
                                    'toolinfo': "Инструмент для поиска общих коротких пептидов (mot) в двух протеомах"},
                      'find_mots': {'toolname': 'Find Mots',
                                    'toolinfo': 'Этот инструмент позволяет найти моты заданого белка в белках любого заданного FASTA протеома. Результаты работы данного инструмента необходимы для создания Block и Build'},
                      'align': {'toolname': 'Align Sequences',
                                'toolinfo': 'Этот инструмент позволяет выровнять две и более последовательностей белка по участку общего сходства'},
                      'block': {'toolname': 'Analyze Block',
                                'toolinfo': 'Инструмент позволяет построить блок - матрицу последовательностей с заданной длинной слева и справа от мота'},
                      'build': {'toolname': 'Build',
                                'toolinfo': 'Работа над этим модулем все еще ведется'}
                  }}

    tab_rus_layout = [[sg.Text('OUROBOROS', justification='center', text_color='blue', size=(70,1), font=('Helvetica', 18))],
                     [sg.Text(info0_text_rus['main'], font=('Courier New', 12), size=(100, (len(info0_text_rus['main'])//100 + 1)))],
                     [sg.Frame(layout=[
                         [sg.Frame(layout=[[sg.Text(info0_text_rus['tools'][i]['toolinfo'],
                                                    font=('Courier New', 12),
                                                    size=(100, (len(info0_text_rus['tools'][i]['toolinfo'])//100 + 1)))]
                                           ],
                                   title_color='red',
                                   font=('Courier New', 15),
                                   title=info0_text_rus['tools'][i]['toolname'])] for i in info0_text_rus['tools'].keys()
                     ], title="Tools", title_color='red', font=('Courier New', 16))]]

    tab_eng_layout = [[sg.Text('OUROBOROS', justification='center', text_color='blue', size=(70,1), font=('Helvetica', 18))],
                     [sg.Text(info0_text['main'], font=('Courier New', 14), size=(100, (len(info0_text['main'])//100 + 1)))],
                     [sg.Frame(layout=[
                         [sg.Frame(layout=[[sg.Text(info0_text['tools'][i]['toolinfo'],
                                                    font=('Courier New', 12),
                                                    size=(100, (len(info0_text['tools'][i]['toolinfo'])//100 + 1)))]
                                           ],
                                   title_color='red',
                                   font=('Courier New', 12),
                                   title=info0_text_rus['tools'][i]['toolname'])] for i in info0_text['tools'].keys()
                     ], title="Tools", title_color='red', font=('Courier New', 16))]]

    layout_info_0 = [[sg.TabGroup([[sg.Tab('English', tab_eng_layout), sg.Tab('Russian', tab_rus_layout)]])],
                     [sg.Button('Back')]]

    window0_info = sg.Window('Information', layout_info_0)

    while True:  # Event Loop
        event0_i, values0_i = window0_info.read()
        # print(event0, values0)
        if event0_i == sg.WIN_CLOSED or event0_i == 'Back':
            break

    window0_info.close()

def find_protein_info():
    import PySimpleGUI as sg
    info_text_rus = {'Main': 'Этот инструмент позволяет провести поиск по ключевым словам в любом FASTA протеоме.',
                     'Proteom': 'Для поиска выберите протеом из списка предложенных в директории приложения /data/proteoms или укажите путь до файла протеома в формате .fasta, нажав кнопку Browse.',
                     'Search keyword': 'Поиск по нескольким ключевым словам на данный момент не реализован. Для более быстрого получения результата рекомендуется осуществлять вывод запроса в файл,'
                      ' так как вывод в окно программы происходит дольше, если поисковому запросу соответствует много объектов протеома.',
                     'Search in': 'Поиск производится по ключевым словам - в названии белка (name), по виду организма (organism), в первичной последовательности (seq), по идентификатору (id). Будьте внимательны - программа чувствительна к регистру (кроме аминокислотного кода, который будет преобразован в верхний регистр)',
                     'Output':'Программа выводит результаты поиска в окно, если не выбран вывод в файл. Поиск через приложение рекомендован для ознакомления и уточнения,'
                              ' тогда как вывод в файл может потребоваться для оценки большого массива данных. По умолчанию файл сохраняется в папке программы по пути /data/user_data'}

    info_text_eng = {'Main': 'Complex search tool for any FASTA proteom. You may choose search parameter (protein name, organism, id, sequence)',
                     'Proteom': 'Add .fasta proteom to /data/user_data/proteoms and select it from list in the application (after restart), or browse it anywhere on your computer',
                     'Search keyword': 'It can be a part of protein name, species name, unique id or sequence. Be careful - search is susceptible to letter case (but all sequences keywords will be automatically turned into uppercase)',
                     'Search in': '.fasta format contains database info, such as protein name, id, species, also it contains protein sequence',
                     'Output': 'You may choose to direct output into the application window either into the txt file. Output file will be saved in the /data/user_data directory by default. '}

    tab_rus_layout = [[sg.Frame(layout=[[sg.Text(info_text_rus[i],
                                                 font=('Courier New', 12),
                                                 size=(100, (len(info_text_rus[i])//100 + 1)))]],
                                title=i, title_color='red', font=('Courier New', 15))] for i in info_text_rus.keys()]

    tab_eng_layout = [[sg.Frame(layout=[[sg.Text(info_text_eng[i],
                                                 font=('Courier New', 12),
                                                 size=(100, (len(info_text_eng[i])//100 + 1)))]],
                                title=i, title_color='red', font=('Courier New', 15))] for i in info_text_eng.keys()]


    layout_info = [[sg.TabGroup([[sg.Tab('English', tab_eng_layout), sg.Tab('Russian', tab_rus_layout)]])],
                     [sg.Button('Back')]]

    window_info = sg.Window('Find protein Info', layout_info)

    while True:  # Event Loop
        event_i, values_i = window_info.read()
        # print(event0, values0)
        if event_i == sg.WIN_CLOSED or event_i == 'Back':
            break

    window_info.close()

def find_mots_info():
    import PySimpleGUI as sg
    info_text_rus = {'Main': 'Данный инструмент используется для поиска мотов белка в заданном протеоме. Найденные моты проходят диффузный поиск (со всеми возможными однобуквенными заменами)'
                             ' и составляют основу для работы Block и Build.',
    'Protein info': 'Введите данные белка. Все поля обязательны для заполнения. В поле ID рекомендуется вводить id белка на портале Uniprot,'
                    ' если таковое имеется, однако можно использовать любую комбинацию символов и букв. Если выбрана опция Make build, после поиска мотов будет произведен диффузный (т.е. со всеми возможными однобуквенными заменами0 поиск'
                    ' в заданном протеоме, а также будет создан объект, содержащий найденные диффузные моты и выровненные белки. Объект доступен во вкладке build основного меню после перезапуска программы. '
                    'Если опция Make block выключена, программа прекратит работу после поиска всех мотов исследуемого белка в заданном протеоме, все найденные моты будут выведены в окно программы.',
    'Proteom': 'Для корректной работы программы выберите протеом в формате .fasta из списка предложенных или используйте свой, указав путь до файла протеома, после нажатия кнопки Browse.',
    'Info': 'Скорость поиска мотов для одного белка напрямую зависит от длины этого белка и от количества белков в протеоме.'
            ' После программа выполняет для каждого из найденных мотов все возможные однобуквенные замены. '
            'Это довольно медленный процесс, который может занять некоторое время. Для получения обратной связи о том,'
            ' что программа работает в нее добвленно двя счетчика прогресса - верхний отражает движение сквозь протеом, нижний - прогресс перебора диффузных мотов'
            ' (т.е. мотов с заменами). В процессе переборки диффузных мотов алгоритм продолжает проходить сквозь протеом, так что данном этапе будут работать оба счетчика прогресса.',
    'Output':' По итогу работы программа создает файл формата .json для каждого исследованного белка.'
             ' Этот файл создается в директории /data/user_data/builds и далее используется для построения Block и Build. Найденные моты программа возdращает в окно вывода перед стартом поиска диффузных мотов.'
             ' Возможность поиска только мотов белка пока не реализована.'}

    info_text_eng = {'Main': 'This tool is useful for searching of mots of one protein in any proteom. Results will be used for Build and Block tools',
                     'Protein info':'',
                     'Proteom':'Add .fasta proteom to /data/user_data/proteoms and select it from list in the application (after restart), or browse it anywhere on your computer',
                     'Info':'',
                     'Output':''}

    tab_rus_layout = [[sg.Frame(layout=[[sg.Text(info_text_rus[i],
                                                 font=('Courier New', 12),
                                                 size=(100, (len(info_text_rus[i])//100 + 1)))]],
                                title=i, title_color='red', font=('Courier New', 15))] for i in info_text_rus.keys()]

    tab_eng_layout = [[sg.Frame(layout=[[sg.Text(info_text_eng[i],
                                                 font=('Courier New', 12),
                                                 size=(100, (len(info_text_eng[i])//100 + 1)))]],
                                title=i, title_color='red', font=('Courier New', 15))] for i in info_text_eng.keys()]

    layout_info = [[sg.TabGroup([[sg.Tab('English', tab_eng_layout), sg.Tab('Russian', tab_rus_layout)]])],
                   [sg.Button('Back')]]

    window_info = sg.Window('Find Mots info', layout_info)

    while True:  # Event Loop
        event_i, values_i = window_info.read()
        # print(event0, values0)
        if event_i == sg.WIN_CLOSED or event_i == 'Back':
            break

    window_info.close()

def compare_proteoms_info():
    import PySimpleGUI as sg
    info_text_rus = {'Main': 'Данный инструмент позволяет найти общие моты в белках двух протеомов',
                     'FROM proteom path': 'Исследуемый протеом (протеом-донор). Для поиска выберите протеом из списка предложенных в директории /data/proteoms или укажите путь до файла протеома в формате .fasta, нажав кнопку Browse.',
                     'TO proteom path': 'Сравниваемый протеом (протеом-реципиент). Для поиска выберите протеом из списка предложенных в директории /data/proteoms или укажите путь до файла протеома в формате .fasta, нажав кнопку Browse.',
                     'Mot lenght': 'Длина рамки поиска (длина мота) от 8 до 12 аминокислот.',
                     'Search way': 'Программа может осуществлять два варианта поиска мотов:\n'
                                   '1.Sequent - используется для последовательного нахождения сходных участков. После нахождения мота он исключается из первоначальной белковой последовательности и в последующем поиске мотов уже не участвует'
                                   'Подходит для поиска всех вохможных мотов заданной длины, исключает перекрытие. Последовательный способ поиска также исключает возможность повторного нахождения мота данного белка протеома-донора в других'
                                   'белках протеома-реципиента'
                                   '2. Casual - этот вариант использовался ранее и позволяет искать участки гомологии любой длины.'
                                   ' Когда найдено совпадение участков заданной длины, алгоритм расширяет рамку считывания до тех пор, пока продолжается участок сходства между белками.'
                                   ' Такой способ предоставляет возможность искать более длинные участки гомологии, нежели участки с установленной длинной,'
                                   ' но при этом возможно нахождение частично перекрывающихся участков сходства в разных белках, то есть моты, минимально отличающиеся друг от друга, что не подходит для построения',
                     'Output file path': 'По умолчанию файл вывода в табличном формате .csv сохраняется в директории /data/user_data, но можно выбрать удобное расположение, нажав кнопку Browse.'}

    info_text_eng = {'main': 'An instrument for search of short peptide called Mot - same region in two or more different sequences',
                     'FROM proteom path': '',
                     'TO proteom path': '',
                     'Mot lenght': '',
                     'Search way': '',
                     'Output file path': ''}

    tab_rus_layout = [[sg.Frame(layout=[[sg.Text(info_text_rus[i],
                                                 font=('Courier New', 12),
                                                 size=(100, (len(info_text_rus[i])//100 + 1) + info_text_rus[i].count('\n')))]],
                                title=i, title_color='red', font=('Courier New', 15))] for i in info_text_rus.keys()]

    tab_eng_layout = [[sg.Frame(layout=[[sg.Text(info_text_eng[i],
                                                 font=('Courier New', 12),
                                                 size=(100, (len(info_text_eng[i])//100 + 1)))]],
                                title=i, title_color='red', font=('Courier New', 15))] for i in info_text_eng.keys()]

    layout_info = [[sg.TabGroup([[sg.Tab('English', tab_eng_layout), sg.Tab('Russian', tab_rus_layout)]])],
                     [sg.Button('Back')]]

    window_info = sg.Window('Compare Proteoms info', layout_info)

    while True:  # Event Loop
        event_i, values_i = window_info.read()
        # print(event0, values0)
        if event_i == sg.WIN_CLOSED or event_i == 'Back':
            break

    window_info.close()

def align_seqs_info():
    import PySimpleGUI as sg
    info_text_rus = {'main':'Этот инструмент позволяет осуществить простое выравнивание двух белков на основании наличия общего участка',
    'info':'Введите название белков и первичную последовательность в соответствющие поля. На данный момент программа совершает простое выравнивание двух белков'
           'на основании наличия общего участка сходства длиной 6 и более аминокислот',
    'output':'Если выбран вывод в файл, можно выбрать имя файла и место для сохранения. Белки будут сохраняться в файл .txt без переносов белковых последовательностей,'
             'что позволит просматривать белки в виде единственной линии. Можно выбрать место сохранения файла, по умолчанию выбрано /data/user_data.'
             'Результаты разных выравниваний будут сохранены в один и тот же файл, если не изменено название и текущее расположение создаваемого файла полностью соотствествует уже'
             'существующему файлу.'}

    info_text_eng = {'main':'',
    'info':'',
    'output':''}

    tab_rus_layout = [[sg.Frame(layout=[[sg.Text(info_text_rus[i],
                                                 font=('Courier New', 12),
                                                 size=(100, (len(info_text_rus[i])//100 + 1)))]],
                                title=i, title_color='red', font=('Courier New', 15))] for i in info_text_rus.keys()]

    tab_eng_layout = [[sg.Frame(layout=[[sg.Text(info_text_eng[i],
                                                 font=('Courier New', 12),
                                                 size=(100, (len(info_text_eng[i])//100 + 1)))]],
                                title=i, title_color='red', font=('Courier New', 15))] for i in info_text_eng.keys()]

    layout_info = [[sg.TabGroup([[sg.Tab('English', tab_eng_layout), sg.Tab('Russian', tab_rus_layout)]])],
                   [sg.Button('Back')]]

    window_info = sg.Window('Find Mots info', layout_info)

    while True:  # Event Loop
        event_i, values_i = window_info.read()
        # print(event0, values0)
        if event_i == sg.WIN_CLOSED or event_i == 'Back':
            break

    window_info.close()

    while True:  # Event Loop
        event_i, values_i = window_info.read()
        # print(event0, values0)
        if event_i == sg.WIN_CLOSED or event_i == 'OK':
            break

    window_info.close()

def analyze_block_info():
    import PySimpleGUI as sg
    info_text_rus = {'Main': 'Block - инструмент, создающий матрицу белковых последовательностей одинаковой длины последовательности варавниваются после поиска диффузных мотов '
                             '(мот заданной длины со всеми возможными однобуквенными заменами)',
                     'Block options': 'В основе блока стоит мот белка. Рамка увеличивается вправо и влево до установленного размера (от 10 до 70) - блок. В каждом из белков,'
                                         'где были найдены диффузные моты, рамка также расширяется и формируются блоки. Белки формируют таблицу, где значения отсотрированы'
                                         'в порядке увеличения времени дивергенции вида (может отображаться не верно)',
                     'Tabs': 'Во вкладке Block представлена таблица блоков, данные по белкам, а также инструменты анализа. '
                             'Во вкладке Positions  приведены сводные данные по каждой из позиций общего блока. Каждая строчка с номером - позиция/столбец из заданной пользователем длины блока'
                             'Данные представлены в виде пары "буква - количество" таких букв в данной позиции в общем блоке со всеми белками',
                     'Analysis tools ': 'Анализ представляет собой последовательный процесс - это значит, что каждый сужающий параметр поиска редуцирует выборку,'
                                        ' представленную в таблице. То есть чтобы начать поиск по другим параметрам необходимо сначала сбросить результат предыдущего поиска, нажав кнопку Clean.'
                                        'Letter Frequency - инструмент позволяет убрать буквы, встречающиеся реже заданного числа раз'
                                        'Опция Splitted позволяет выводить последовательности в столбце block c разбитием по 10, что может быть удобно'
                                        'для выбора белков, имеющих определенную букву в заданной позиции. Чтобы выбрать только белки,'
                                        ' имеющие только определенную букву в заданной позиции, введите букву и ее позицицию в блоке в поля Letter и Position соответственно.'
                                        'Обратите внимание, что ширину столбцов можно изменять, для этого следует навестись на перегородку между столбцами в шапке таблицы.',
                     'Copy and output': 'После нажатия кнопки Save текущая выборка сохранится в папке /data/User_data. Можно выбрать белок (или несколько)'
                                        ' и, нажав кнопку Copy, вывести полную информацию по белку для ее просмотра или копирования'}

    info_text_eng = {'Main': 'Block tool allows you to choose region around mot in a group of proteins aligned by mot',
                     'Block options': '',
                     'Tabs': '',
                     'Analysis tools ': '',
                     'Copy and output': ''}

    tab_rus_layout = [[sg.Frame(layout=[[sg.Text(info_text_rus[i],
                                                 font=('Courier New', 12),
                                                 size=(100, (len(info_text_rus[i])//100 + 1)))]],
                                title=i, title_color='red', font=('Courier New', 15))] for i in info_text_rus.keys()]

    tab_eng_layout = [[sg.Frame(layout=[[sg.Text(info_text_eng[i],
                                                 font=('Courier New', 12),
                                                 size=(100, (len(info_text_eng[i])//100 + 1)))]],
                                title=i, title_color='red', font=('Courier New', 15))] for i in info_text_eng.keys()]

    layout_info = [[sg.TabGroup([[sg.Tab('English', tab_eng_layout), sg.Tab('Russian', tab_rus_layout)]])],
                     [sg.Button('Back')]]

    window_info = sg.Window('Analyze block Info', layout_info)

    while True:  # Event Loop
        event_i, values_i = window_info.read()
        if event_i == sg.WIN_CLOSED or event_i == 'Back':
            break

    window_info.close()

def make_build_info():
    import PySimpleGUI as sg
    info_text_rus = {'main':'',
    'info':'',
    'output':''}

    info_text_eng = {}

    tab_rus_layout = [[sg.Frame(layout=[[sg.Text(info_text_rus[i],
                                                 font=('Courier New', 12),
                                                 size=(100, (len(info_text_rus[i])//100 + 1)))]],
                                title=i, title_color='red', font=('Courier New', 15))] for i in info_text_rus.keys()]

    tab_eng_layout = [[sg.Frame(layout=[[sg.Text(info_text_eng[i],
                                                 font=('Courier New', 12),
                                                 size=(100, (len(info_text_eng[i])//100 + 1)))]],
                                title=i, title_color='red', font=('Courier New', 15))] for i in info_text_eng.keys()]

    layout_info = []

    window_info = sg.Window('Make build info', layout_info)

    while True:  # Event Loop
        event_i, values_i = window_info.read()
        # print(event0, values0)
        if event_i == sg.WIN_CLOSED or event_i == 'OK':
            break

    window_info.close()



