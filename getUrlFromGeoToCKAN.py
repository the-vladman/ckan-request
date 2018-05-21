import requests
import json
import os
from dotenv import load_dotenv
import pymongo

load_dotenv()

GEOSERVER_URL= os.getenv('GEOSERVER_URL')
GEOSERVER_USER= os.getenv('GEOSERVER_USER')
GEOSERVER_PASSWORD= os.getenv('GEOSERVER_PASSWORD')
MONGO_URL= os.getenv('MONGO_URL')
MONGO_PORT= os.getenv('MONGO_PORT')

mongoClient = pymongo.MongoClient(MONGO_URL, int(MONGO_PORT))
dbBuda = mongoClient.buda
geoCollection = dbBuda['ckan-geoserver']


headers = {'accept':'application/json'}
r = requests.get(GEOSERVER_URL,headers=headers, auth=(GEOSERVER_USER, GEOSERVER_PASSWORD))
response = r.json()

layers = response['layers']
layersArray = layers['layer']

for layer in layersArray:
    name = layer['name']
    nameSliced = name[0:36]
    nameReplaced = nameSliced.replace('_', '-')
    layerAdd = {'ckan':nameReplaced, 'geoserver':layer['name']}
    geoCollection.save(layerAdd)