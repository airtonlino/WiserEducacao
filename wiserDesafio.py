import pandas as pd
import json
import csv
import requests
import io
import shutil
import os
from pandas.io.json import json_normalize
from googleapiclient.http import MediaIoBaseDownload
from __future__ import print_function

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

files = DRIVE.files().list().execute().get('files', [])
lista = []
nomeArquivo = []
for f in files:
  fileName = f['name']
  if 'acervo_' in fileName:
    #lista.append(f['id'])
    #nomeArquivo.append(f['name'])

    file_id = f['id']
    file_name = f['name']
    caminho = '/content/'+file_name
    caminhoCSV = caminho+'.csv'
    caminhoCSV300 = caminho+'300'+'.csv'

    if os.path.exists(caminho):
      #Deleta arquivo se existir
      os.remove(caminho)
    if os.path.exists(caminhoCSV):
      #Deleta arquivo se existir
      os.remove(caminhoCSV)
    if os.path.exists(caminhoCSV300):
      #Deleta arquivo se existir
      os.remove(caminhoCSV300)
      
    #Cria arquivo em branco
    f = open(caminho, "x")
    #Download do arquivo
    request = DRIVE.files().get_media(fileId=file_id)
    fh = io.BytesIO ()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
      status, done = downloader.next_chunk()
    fh.seek(0)
    with open(caminho, 'wb') as f:
      shutil.copyfileobj(fh, f)

    #Lê o arquivo JSON
    registros = pd.read_json(caminho,typ='frame')
    #Normaliza
    registrosNormalizado = pd.json_normalize(registros['_default'])
    #registrosNormalizado.head(2) 
    #Gera CSV 
    registrosNormalizado.to_csv(caminhoCSV,index=True)
    #Gera CSV com as 300 primeiras linhas
    trezentaslinhas = registrosNormalizado.head(300) 
    trezentaslinhas.to_csv(caminhoCSV300,index=True)
