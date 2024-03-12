import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

def verificarThreads(numero:int,timestep:int):
    load_dotenv()
    url = "https://api.airtable.com/v0/appbxRoCE8BNBtQp8/threads"
    authToken = os.getenv('BEARER')

    headers = {"Authorization": f"Bearer {authToken}"}
    data = requests.get(url, headers=headers).json()
    for record in data['records']:
        if 'number' in record['fields'] and record['fields']['number'] == numero:
            timesBaseDeDatos = record['fields']['timestep']
            if timesBaseDeDatos > timestep:
                return False
            new = {'fields':{'timestep':timestep}}
            requests.patch(url+'/'+record['id'],headers=headers,json=new)
            return record['fields']['threads']
    #crear hilo
    KEY_OPENAI = os.getenv('KEY_OPENAI')
    client = OpenAI(api_key=KEY_OPENAI)
    hilo = client.beta.threads.create()
    new = {'fields':{'number':numero,'threads':hilo.id,'timestep':timestep}}
    requests.post(url,headers=headers,json=new)
    return hilo.id