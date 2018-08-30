import json
from bson import json_util
import os
from dotenv import load_dotenv
import pymongo
import csv
import sys
import ckanapi

reload(sys)
sys.setdefaultencoding('utf8')
load_dotenv()

CKAN_HOST = os.getenv('CKAN_HOST')
CKAN_TOKEN = os.getenv('CKAN_API_TOKEN')
MONGO_URL= os.getenv('MONGO_URL')
MONGO_PORT= os.getenv('MONGO_PORT')
COUNTER = 0

file = open("APIionCollects.csv","w")
fieldnames = ['ID', 'IDCKAN', 'IDGEO']
writer = csv.DictWriter(file, fieldnames=fieldnames)
writer.writeheader()

mongoClient = pymongo.MongoClient(MONGO_URL, int(MONGO_PORT))
dbBuda = mongoClient.buda
geoCollection = dbBuda['ckan-geoserver']
remote = ckanapi.RemoteCKAN(CKAN_HOST, user_agent='ckanops/1.0', apikey=CKAN_TOKEN)

def getDatasetFromCKAN(remote, idDataset):
    try:
        dataset = remote.action.package_show(id=idDataset)
        return True
    except ckanapi.errors.CKANAPIError:
        return False

def getResourceFromCKAN(remote, idResource):
    try:
        resource = remote.action.resource_show(id=idResource)
        return True
    except ckanapi.errors.CKANAPIError as e:
        return False


for c in geoCollection.find():
    if getResourceFromCKAN(remote, c['ckan']):
        COUNTER += 1
        collection = {'ID': COUNTER, 'IDCKAN': c['ckan'], 'IDGEO': c['geoserver']}
        writer.writerow(collection)
        print COUNTER , 'Collection Added'