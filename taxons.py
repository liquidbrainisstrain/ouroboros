import sqlite3
import pydot

final_tree = {}

def getRows(name):
    cur.execute("SELECT id FROM taxons WHERE name=?", (name,))
    id = cur.fetchone()[0]
    cur.execute("SELECT name, diverg FROM taxons JOIN divergence ON id = second_id WHERE first_id = ? GROUP BY name", (id,))
    rows = cur.fetchall()
    return rows

def adoptChild(lst, to_node):
    if not lst:
        return to_node
    else:
        ch = lst.pop()
        to_node[ch] = {}
        return adoptChild(lst, to_node[ch])

def draw(parent_name, child_name):
    edge = pydot.Edge(parent_name, child_name)
    graph.add_edge(edge)

def visit(node, parent=None):
    for k,v in node.items():
        if isinstance(v, dict):
            if parent:
                draw(parent, k)
            visit(v, k)
        else:
            draw(parent, k)
            draw(k, k+'_'+v)

conn = sqlite3.connect('bacteries.db')
cur = conn.cursor()

first_taxon =input('Введи первый таксон, SUKA ')
second_taxon = input('А теперь второй, MRAZ ')

fst = set(getRows(first_taxon) + [(first_taxon, 0)])
snd = set(getRows(second_taxon) + [(second_taxon, 0)])

common = fst & snd
fst = sorted(list(fst ^ common), key = lambda x: x[1])
snd = sorted(list(snd ^ common), key = lambda x: x[1])
com = sorted(list(common), key = lambda x: x[1])

parent_lst = [el[0] + ": " + str(el[1]) + " MYA" for el in com]
fst_lst = [el[0] + ": " + str(el[1]) + " MYA" for el in fst]
snd_lst = [el[0] + ": " + str(el[1]) + " MYA" for el in snd]

bifurc = adoptChild(parent_lst, final_tree)
adoptChild(fst_lst, bifurc)
adoptChild(snd_lst, bifurc)

graph = pydot.Dot(graph_type='graph')
visit(final_tree)
graph.write_png('final_tree.png')
