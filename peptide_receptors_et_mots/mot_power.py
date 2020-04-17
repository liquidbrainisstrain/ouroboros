from modules import mot_changer as mch
from pymongo import MongoClient

filename = '/Users/liquidbrain/Desktop/motpowerres.txt'
#db init
client = MongoClient()
db = client.proteins
all_proteins = db.gen_proteom_beta
arc_mots = db.archea_mots
proteoms = [i for i in all_proteins.find()]

seq1 = 'MVIKKMQPEDLTENDIRRFADSKRIFGRGESYYRRGKIRSMDVSRDKKEITAKVDGNYGIYDVEIYFDEDGISADCDCPYDGYGCKHIVAVLLEFLYEFKGDKKDNEDEEPWDITLEDIRGHTSKQSILDAFDLLKEKKVEIKSLTNKRMTAEIDEKITRHTYPWQKDIVGNAMVKITRGNYNLSYPLGTECNCTGYGRADCKHVAASLLAIFLQKNKKQISEVKEEFISQIRSERFNRFTRELDSISLEEPKVKHTRNYMFYFKAEKDTRPYSKFSLLIEKRCILKSCGLGTPSQVTTKFLKEYEDTIPNNRKRIFNSFIWSLENEERWRSSSEKLIKQNFKESDSKLLAEMRKLYMADPHAFENCVFPSEKGEIEIKISEEKKRKKSVLKLMVNIGEKKFQINKKNVTFLGKHPLWVSIFENEKNGFIIFELDCSQPEIIKKLAGFSNAELELNQLNAFIEKYYLTLSAIGKITLPENYDVEEQRFEPVPRLFLRDYGTSFSIELRFLYDKQEVLYTQKQDIVFKNDREKIIRIQRDREKEKEYFANLLDHHTTDCDDFLVPATDPYLWLVDVANDLITRGYEIYGASELLNTRIAPHEPKLRLEVSSGIDWFDLKGDVSYGAEKVPFDEIISHVNNHERFVKLSDGTRGVIPKKWLEKLSGTVGLLERDEKNGNAKASRSQIALVEALLDISEKSRVDKRFKQMKEKFSGFREIRNVSLPKKLDGELREYQKAGYDWLHFLKDFSFGGCLADEMGLGKTVQALSLLLYEKERGIKTPSLVVVPTSLVFNWVNEVKKFTPSLKVYIHHGSERVREGKQIWKKKANIILTTYGTLRNDANIFKNKKFHYVILDESQHIKNPLSKTAKKIYGLKSKHKLAMTGTPIENNSFELWSQFAFLNPGLLGNMDYFKKNFAKSIEKEKDEDKTKALKNMINPFLLMRKKEMVAKDLPEKQISVSYCEMDRKQREVYEFWKSRIRNEIETTIKEEGFMKSRFKILQGLMKLRQICNHPVLVDESFTGDSGKLNMLMEQIEEVIAEGHKVLVFSSFVKMLGVFRGEFERKGIRFSYLDGSTRNRKQVVEQFQEDPDMRAFLISLKAGGLGLNLTEADYVFIVDPWWNPAAEMQAIDRTHRIGQEKNIFVYKAITKDSIEEKILQLQESKLDLVKNVIAVDDGLFKKLNKEDINKLFA'
mot1 = 'LADEMGLGKTVQ'
suc_mots = ['VADEMGLGKTVQ', 'LADDMGLGKTVQ', 'LADEAGLGKTVQ', 'LADEMGLGKSVQ', 'LADEMGLGKTAQ', 'LADEMGLGKTLQ', 'LADEMGLGKTIQ', 'LADEMGLGKTCQ', 'LADEMGLGKTVE', 'LADEMGLGKTVS']
all_mots = []
for i in suc_mots:
    for var in mch(i):
        all_mots.append(var)
c = 1
all_mots = list(set(all_mots))
suc_mots = []
for mot in all_mots:
    for prot in proteoms:
        if mot in prot['seq']:
            suc_mots.append(mot)
    print(c, 'done')
    c+=1

print(len(suc_mots))
print(len(list(set(suc_mots))))
print(list(set(suc_mots)))




# print(arc_prots_and_mots)
#
# with open(filename, 'w') as file:
#     line = "Результаты проверки измененных на 1 а.к. мотов в общем протеоме\n"
#     file.write(line)
#     items_c = 1
#     for item in arc_prots_and_mots:
#         mot = item['mots'][0]
#         line = "Проверка вариантов мота " + mot + '\n'
#         file.write(line)
#         changed = mch(mot)
#         c = 1
#         for chan in changed:
#             for protein in proteoms:
#                 if protein['seq'].count(chan) > 0:
#                     line = "Mot - {} was found in protein {}, organism {} \n {}\n  \n".format(
#                         chan, protein['name'], protein['organism'], protein['seq'])
#                     file.write(line)
#             print(c, 'of', len(changed), 'done')
#             c+=1
#         print('--------', mot, 'number', items_c, 'of all', len(arc_prots_and_mots), 'done')
#         items_c += 1

