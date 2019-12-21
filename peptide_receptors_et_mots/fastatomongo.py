from modules import fasta_parser as fp
from modules import mot_finder as mf
import pprint
from pymongo import MongoClient
import time
import collections

#db init
client = MongoClient()
db = client.proteins


line1 = str(input("введи строку "))
print(len(line1))

