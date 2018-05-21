import os
import ckanapi
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv('CKAN_HOST')
TOKEN = os.getenv('CKAN_API_TOKEN')
DATASET = os.getenv('DATASET_TO_UPDATE')

def getDataset(remote, idDataset):
    try:
        dataset = remote.action.package_show(id=idDataset)
        return dataset['id']
    except ckanapi.errors:
        print 'ERROR'

remote = ckanapi.RemoteCKAN(HOST, user_agent='ckanops/1.0', apikey=TOKEN)        

dataset = getDataset(remote, DATASET)