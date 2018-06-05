import requests
import json
import os
from dotenv import load_dotenv
import pymongo
import ckanapi

load_dotenv()

CKAN_HOST = os.getenv('CKAN_HOST')
CKAN_TOKEN = os.getenv('CKAN_API_TOKEN')
GEOSERVER_URL= os.getenv('GEOSERVER_URL')
GEOSERVER_USER= os.getenv('GEOSERVER_USER')
GEOSERVER_PASSWORD= os.getenv('GEOSERVER_PASSWORD')
MONGO_URL= os.getenv('MONGO_URL')
MONGO_PORT= os.getenv('MONGO_PORT')

mongoClient = pymongo.MongoClient(MONGO_URL, int(MONGO_PORT))
dbBuda = mongoClient.buda
geoCollection = dbBuda['ckan-geoserver']
remote = ckanapi.RemoteCKAN(CKAN_HOST, user_agent='ckanops/1.0', apikey=CKAN_TOKEN)

headers = {'accept':'application/json'}
r = requests.get(GEOSERVER_URL,headers=headers, auth=(GEOSERVER_USER, GEOSERVER_PASSWORD))
response = r.json()

layers = response['layers']
layersArray = layers['layer']

def getDatasetFromCKAN(remote, idDataset):
    try:
        dataset = remote.action.package_show(id=idDataset)
        return dataset
    except ckanapi.errors.CKANAPIError:
        pass

def getResourceFromCKAN(remote, idResource):
    try:
        resource = remote.action.resource_show(id=idResource)
        return resource
    except ckanapi.errors.CKANAPIError as e:
        pass

def getCategoryFromDataset(extras):
    for e in extras:
        if e['key'] == 'theme':
            return e['value']
        else:
            return 'no'

def getTagsFromDataset(dataset):
    if dataset['tags']:
        return dataset['tags']
    else:
        return []

def getOrganizationFromDataset(dataset):
    if dataset['organization']:
        return dataset['organization']
    else:
        return 'no-organization'


for layer in layersArray:
    name = layer['name']
    nameSliced = name[0:36]
    nameReplaced = nameSliced.replace('_', '-')
    resourceCKAN = getResourceFromCKAN(remote, nameReplaced)
    layerAdd = {'ckan':nameReplaced, 'geoserver':layer['name']}
    if resourceCKAN:
        datasetCKAN = getDatasetFromCKAN(remote, resourceCKAN['package_id'])
        category = getCategoryFromDataset(datasetCKAN['extras'])
        tags = getTagsFromDataset(datasetCKAN)
        organization = getOrganizationFromDataset(datasetCKAN)
        layerMetadata = {'name_resource':resourceCKAN['name'], 'tags': tags, 'organization': organization, 'category': category}
        layerAdd.update(layerMetadata)
    print layerAdd
    geoCollection.save(layerAdd)