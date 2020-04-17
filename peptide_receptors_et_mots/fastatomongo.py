from pymongo import MongoClient

#db init
client = MongoClient()
db = client.proteins


line1 = str(input("введи строку "))
print(len(line1))

