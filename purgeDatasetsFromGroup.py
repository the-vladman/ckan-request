import os
import ckanapi
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv('CKAN_HOST')
TOKEN = os.getenv('CKAN_API_TOKEN')
ORG= os.getenv('ORG_TO_PURGE')

file = open("idFiles.txt","w") 

def getOrgDatasets(remote, org):
    try:
        org = remote.action.organization_show(id=org, include_datasets='true')
        return org['packages']
    except ckanapi.NotFound:
        print 'Not Found'
        pass

def getDataset(remote, idDataset):
    try:
        dataset = remote.action.package_show(id=idDataset)
        return dataset['id']
    except ckanapi.errors.CKANAPIError:
        pass

def purgeDataset(remote, idDataset):
    try:
        remote.action.dataset_purge(id=idDataset)
        return 'Deleted'
    except ckanapi.errors.NotAuthorized:
        print 'Not Purge'
        pass

remote = ckanapi.RemoteCKAN(HOST, user_agent='ckanops/1.0', apikey=TOKEN)
org = remote.action.organization_show(id=ORG)
print org['id']
orgDatasets = getOrgDatasets(remote, org['id'])
print len(orgDatasets)
for d in orgDatasets:
    if getDataset(remote, d['id']):
        datasetFound = getDataset(remote, d['id'])
        print datasetFound + ' FOUND TO DELETE'
        purgeDataset(remote, datasetFound)
    else:
        print 'NOT FOUND '+ d['id']
        file.write(d['id'] + '\n')

file.close()