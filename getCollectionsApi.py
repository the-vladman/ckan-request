import json
from bson import json_util
import os
from dotenv import load_dotenv
import pymongo
import sys

reload(sys)
sys.setdefaultencoding('utf8')
load_dotenv()

MONGO_URL= os.getenv('MONGO_URL')
MONGO_PORT= os.getenv('MONGO_PORT')

COUNTER = 0
mongoClient = pymongo.MongoClient(MONGO_URL, int(MONGO_PORT))
dbBuda = mongoClient.buda
allCollections = dbBuda.collection_names()



with open("data_file.json", "w") as write_file:
    for c in allCollections:
        COUNTER += 1
        collection = {'collectionName': c, 'example': dbBuda[c].find_one()}
        json.dump(collection, write_file, default=json_util.default)
        print COUNTER , 'Collection Added'