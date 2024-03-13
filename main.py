import datetime
from fastapi import FastAPI, Request,HTTPException
from dataBot import data
from models.structureMsg import strucMsg
from response import response, responseWSP
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from heyoo import WhatsApp
app = FastAPI()


@app.get('/')
def root():
    load_dotenv()
    URLAuth = os.getenv('URLAUTHENTIC')
    return {'url_athentic':URLAuth}
@app.post('/')
def root(strucMsg:strucMsg):
    print(strucMsg)
    data = response(strucMsg)
    print(data)
    return data
@app.get('/getData')
def dataBot():
    return data()

@app.api_route("/webhook/", methods=["POST", "GET"],status_code=201)

async def logica(request: Request):
    load_dotenv()
    IDENTIFICAR_WSP = os.getenv('IDENTIFICAR_WSP')
    PALABRA_CLAVE = os.getenv('PALABRA_CLAVE')
    PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
    if request.method == "GET":
        if request.query_params.get('hub.verify_token') == PALABRA_CLAVE:
            return int(request.query_params.get('hub.challenge'))
        else:
            raise HTTPException(status_code=401, detail="Error de autenticación.")
    #quiero recibir el mensaje de whatsApp en DATA
    try:
        data = await request.json()
        timestamp = int(data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp'])
        data = data['entry'][0]['changes'][0]['value']['messages'][0]
        mensaje = data['text']['body']
        telefono = int(data['from'])
        try:
            res = await responseWSP(telefono,mensaje,timestamp)
            print(res['mesagge'])
            mensaje = res['mesagge']
            wsp = WhatsApp(IDENTIFICAR_WSP,PHONE_NUMBER_ID)
            numeroAutorizados = {
                5493512450192:543512450192,
                5493513997175:543513997175
                }
            wsp.send_message(mensaje,numeroAutorizados[telefono]) 
            return True
        except Exception as e:
            print(f"Hubo un error al ejecutar responseWSP: {e}")
            return HTTPException(500, detail=str(e))        
    except KeyError as e:
        return HTTPException(500,detail='no se envio en formato mensaje')
    
