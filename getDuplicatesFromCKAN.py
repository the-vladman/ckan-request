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
DKAN_HOST = os.getenv('DKAN_HOST')
CKAN_TOKEN = os.getenv('CKAN_API_TOKEN')

file = open("comparativaCKANvsDKAN.csv","w")
fieldnames = ['ID_DKAN', 'Found_ID_CKAN', 'Found_NAME_CKAN']
writer = csv.DictWriter(file, fieldnames=fieldnames)
writer.writeheader()

def getDatasetFromCKAN(remote, idDataset):
    try:
        resource = remoteCKAN.action.package_show(id=idDataset)
        return 'yes'
    except ckanapi.errors.CKANAPIError as e:
        return 'not'

def getResourceFromCKAN(remote, idResource):
    try:
        resource = remoteCKAN.action.resource_show(id=idResource)
        return 'yes'
    except ckanapi.errors.CKANAPIError as e:
        return 'not'


def getResources():
    try:
        requestAPI = requests.get(DKAN_HOST + '/api/3/action/current_package_list_with_resources')
        response = requestAPI.json()
        results = response['result'][0]
        return results
    except requests.exceptions as e:
        print 'ERROR' + e


remoteCKAN = ckanapi.RemoteCKAN(CKAN_HOST, user_agent='ckanops/1.0', apikey=CKAN_TOKEN)
resources = getResources()

for resource in resources:
    resourceIDFound = getResourceFromCKAN(remoteCKAN, resource['id'])
    resourceNameFound = getResourceFromCKAN(remoteCKAN, resource['name'])
    print(resourceNameFound)
    row = {'ID_DKAN': resource['id'], 'Found_ID_CKAN': resourceIDFound, 'Found_NAME_CKAN':resourceNameFound }
    writer.writerow(row)

file.close()