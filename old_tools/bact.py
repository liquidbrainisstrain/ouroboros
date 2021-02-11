import requests
import time
import sqlite3
from lxml import html


def getElem(bacteria):
    url = "http://www.timetree.org/ajax/name/timeline/" + bacteria + "?select_tag_id=timeline-resolve-target"
    content = requests.get(url).text
    tree = html.fromstring(content)
    num = tree.xpath("//div/div/select/option/@value")[0]

    url2 = "http://www.timetree.org/ajax/timeline/" + num + "?taxon=" + bacteria + "&selected=" + num
    content2 = requests.get(url2).text
    tree2 = html.fromstring(content2)
    values = tree2.xpath("//svg[7]/text/text()")
    final_value = [(values[i], values[i + int(len(values) / 2)]) for i in range(int(len(values) / 2)) if
                   values[i + int(len(values) / 2)] != '0']
    return final_value


start = time.time()
common_dict = {}
f = open("spisok.txt", "r")
lst = [(line.strip()).split(" ")[0] for line in f]
lst = set(map(lambda x: x if ord(x[0]) != 12 else x[1:], filter(lambda el: len(el) > 1, lst)))
print(len(lst))
for bact in lst:
    try:
        common_dict[bact] = getElem(bact)
    except IndexError:
        continue
f.close()

conn = sqlite3.connect('bacteries.db')
c = conn.cursor()
c.execute('''CREATE TABLE if not exists taxons(id INTEGER PRIMARY KEY AUTOINCREMENT, name CHAR(30) NOT NULL, UNIQUE(name))''')
c.execute('CREATE INDEX bact_name on taxons(name)')
c.execute('''CREATE TABLE if not exists divergence (first_id INTEGER, second_id INTEGER, diverg INTEGER,
              FOREIGN KEY (first_id) REFERENCES taxons(id), FOREIGN KEY (second_id) REFERENCES taxons(id),
              PRIMARY KEY (first_id, second_id))''')

for key in common_dict:
    c.execute("SELECT * FROM taxons WHERE name = (?)", (key,))
    if not c.fetchone():
        c.execute("INSERT INTO taxons (name) VALUES (?)", (key,))
    for values in common_dict[key]:
        c.execute("SELECT * FROM taxons WHERE name = (?)", (values[0],))
        if not c.fetchone():
            c.execute("INSERT INTO taxons (name) VALUES (?)", (values[0],))

for key in common_dict:
    for name, date in common_dict[key]:
        c.execute("SELECT id FROM taxons WHERE name=?", (key,))
        child_id = c.fetchone()[0]
        c.execute("SELECT id FROM taxons WHERE name=?", (name,))
        parent_id = c.fetchone()[0]
        c.execute('''INSERT INTO divergence (first_id, second_id, diverg) VALUES
                      (?, ?, ?)''', (child_id, parent_id, date,))

conn.commit()
conn.close()
end = time.time()
print("{0:.2f} seconds".format(end - start))