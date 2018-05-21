import os
import ckanapi
from dotenv import load_dotenv
import requests

load_dotenv()
CKAN_HOST = os.getenv('CKAN_HOST')
CKAN_TOKEN = os.getenv('CKAN_API_TOKEN')
API_URL= os.getenv('API_URL')
COLLECTION_NAME= os.getenv('COLLECTION_NAME')

def getDatasetFromCKAN(remote, idDataset):
    try:
        dataset = remote.action.package_show(id=idDataset)
        return dataset['id']
    except ckanapi.errors.CKANAPIError:
        pass

def getResourceFromCKAN(remote, idResource):
    try:
        dataset = remote.action.package_show(id=idResource)
        return dataset['id']
    except ckanapi.errors.CKANAPIError:
        pass

def getAPIResources(page,pageSize):
    try:
        params = {'page': page, 'pageSize':pageSize}
        requestAPI = requests.get(API_URL + COLLECTION_NAME, params)
        response = requestAPI.json()
        results = response['results']
        return results
    except:
        print 'error'

remote = ckanapi.RemoteCKAN(CKAN_HOST, user_agent='ckanops/1.0', apikey=CKAN_TOKEN)



resourcesToVerify = getAPIResources(1, 1000)

print len(resourcesToVerify)