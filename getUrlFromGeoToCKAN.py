import requests
import json
import os
from dotenv import load_dotenv
import pymongo
import ckanapi
import sys

reload(sys)
sys.setdefaultencoding('utf8')
load_dotenv()

CKAN_HOST = os.getenv('CKAN_HOST')
CKAN_TOKEN = os.getenv('CKAN_API_TOKEN')
GEOSERVER_URL= os.getenv('GEOSERVER_URL')
GEOSERVER_USER= os.getenv('GEOSERVER_USER')
GEOSERVER_PASSWORD= os.getenv('GEOSERVER_PASSWORD')
MONGO_URL= os.getenv('MONGO_URL')
MONGO_PORT= os.getenv('MONGO_PORT')

COUNTER = 0
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
    return ''

def getTagsFromDataset(dataset):
    if 'tags' in dataset:
        return dataset['tags']
    else:
        return []

def getDescriptionFromResource(resource):
    if 'description' in resource:
        return resource['description']
    else:
        return ''

def getOrganizationFromDataset(dataset):
    if dataset['organization']:
        return dataset['organization']
    else:
        return ''


for layer in layersArray:
    COUNTER += 1
    name = layer['name']
    nameSliced = name[0:36]
    nameReplaced = nameSliced.replace('_', '-')
    resourceCKAN = getResourceFromCKAN(remote, nameReplaced)
    layerAdd = {'ckan':nameReplaced, 'geoserver':layer['name']}
    if resourceCKAN:
        datasetCKAN = getDatasetFromCKAN(remote, resourceCKAN['package_id'])
        category = getCategoryFromDataset(datasetCKAN['extras'])
        tags = getTagsFromDataset(datasetCKAN)
        description = getDescriptionFromResource(resourceCKAN)
        organization = getOrganizationFromDataset(datasetCKAN)
        layerMetadata = {'name_resource':resourceCKAN['name'], 'tags': tags, 'description': description, 'organization': organization, 'category': category}
        layerAdd.update(layerMetadata)
    geoCollection.save(layerAdd)
    print COUNTER , 'Layer Added', layerAdd['ckan']