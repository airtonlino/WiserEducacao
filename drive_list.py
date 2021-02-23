from __future__ import print_function

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import os


#Cria arquivo em branco do storage.json
if os.path.exists('storage.json'):
  #Deleta arquivo se existir
  os.remove('storage.json')
f = open('storage.json', "x")


SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

files = DRIVE.files().list().execute().get('files', [])
for f in files:
    print(f['name'], f['mimeType'])
    
    