import json
from bson import json_util
import os
from dotenv import load_dotenv
import pymongo
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf8')
load_dotenv()

MONGO_URL= os.getenv('MONGO_URL')
MONGO_PORT= os.getenv('MONGO_PORT')
COUNTER = 0

file = open("APICollections.csv","w")
fieldnames = ['ID', 'CollectionName', 'Documented']
writer = csv.DictWriter(file, fieldnames=fieldnames)
writer.writeheader()

mongoClient = pymongo.MongoClient(MONGO_URL, int(MONGO_PORT))
dbBuda = mongoClient.buda
allCollections = dbBuda.collection_names()


for c in allCollections:
    if c.find('ckan.') < 0:
        print c.find('ckan.')
        COUNTER += 1
        collection = {'ID': COUNTER, 'CollectionName': c}
        writer.writerow(collection)
        print COUNTER , 'Collection Added'