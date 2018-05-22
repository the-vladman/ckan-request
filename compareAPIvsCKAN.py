import os
import ckanapi
from dotenv import load_dotenv
import requests
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf8')
load_dotenv()

CKAN_HOST = os.getenv('CKAN_HOST')
CKAN_TOKEN = os.getenv('CKAN_API_TOKEN')
API_URL= os.getenv('API_URL')
COLLECTION_NAME= os.getenv('COLLECTION_NAME')

file = open("comparativaCKANvsAPI.csv","w")
fieldnames = ['ID_API', 'Resource_Name_CKAN', 'Found_CKAN']
writer = csv.DictWriter(file, fieldnames=fieldnames)
writer.writeheader()

def getDatasetFromCKAN(remote, idDataset):
    try:
        dataset = remote.action.package_show(id=idDataset)
        return dataset['id']
    except ckanapi.errors.CKANAPIError:
        pass

def getResourceFromCKAN(remote, idResource):
    try:
        resource = remote.action.resource_show(id=idResource)
        return 'found'
    except ckanapi.errors.CKANAPIError as e:
        return 'not found'

def getAPIResources(page,pageSize):
    try:
        params = {'page': page, 'pageSize':pageSize}
        requestAPI = requests.get(API_URL + COLLECTION_NAME, params)
        response = requestAPI.json()
        results = response['results']
        return results
    except requests.exceptions as e:
        print 'ERROR' + e

totalResources = 34765
page = 1
pageSize = 3000
divideTotal = 12

remote = ckanapi.RemoteCKAN(CKAN_HOST, user_agent='ckanops/1.0', apikey=CKAN_TOKEN)

while page < divideTotal:
    print page
    resourcesToVerify = getAPIResources(page, pageSize)
    for resource in resourcesToVerify:
        resourceToVerify = getResourceFromCKAN(remote, resource['id'])
        nameResource = ''
        if 'name' in resource:
             nameResource = resource['name']
        else:
            nameResource = 'Sin nombre'
        row = {'ID_API': resource['id'], 'Resource_Name_CKAN': nameResource, 'Found_CKAN':resourceToVerify }
        writer.writerow(row)
    page = page + 1
    print page

file.close()