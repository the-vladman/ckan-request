import os
from ckanapi import RemoteCKAN
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('CKAN_HOST')
TOKEN = os.getenv('CKAN_API_TOKEN')
ORG= os.getenv('ORG_TO_PURGE')
remote = RemoteCKAN(HOST, user_agent='ckanops/3.0', apikey=TOKEN)
org = remote.action.organization_show(id=ORG)
print org
orgDatasets = remote.action.organization_show(id=ORG,include_datasets='true')

for d in orgDatasets['packages']:
    print d['id']
    remote.action.dataset_purge(id=d['id'])


