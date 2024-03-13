from fastapi import HTTPException
from openai import OpenAI
from dotenv import load_dotenv
from models.structureMsg import strucMsg
import os
from threads import verificarThreads


def response(strucMsg:strucMsg):
    load_dotenv()
    KEY_OPENAI = os.getenv('KEY_OPENAI')
    ASISTANT = os.getenv('ASISTANT')   

    Client = OpenAI(api_key=KEY_OPENAI)
    asistente = Client.beta.assistants.retrieve(ASISTANT)
    if strucMsg.thread is None:
        thread = Client.beta.threads.create()
    else:
        thread = Client.beta.threads.retrieve(strucMsg.thread)
    try:
        Client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=strucMsg.msg
        )
        run = Client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=asistente.id)
        while run.status not in ["completed","failed"]:
            run = Client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
            )
            #aca poner si requiere una accion el bot
        run_steps = Client.beta.threads.runs.steps.list(
            run_id=run.id,
            thread_id=thread.id
            )
        messages= Client.beta.threads.messages.list(
        thread_id=thread.id
        )
    except Exception as e:
        return HTTPException(500, detail=str(e))


    for mesagge in messages:
        return {
            'mesagge':mesagge.content[0].text.value,
            'thread': thread.id
            }
    


async def responseWSP(numero:int, msg:str,timestep:int):
    print(numero)
    print(msg)
    thread = verificarThreads(numero,timestep)
    if not thread:
        raise HTTPException(status_code=400,detail='Mensaje ya enviado')
    
    print(thread)
    #Crear un objeto strucMsg
    mensaje_estructurado = strucMsg(msg=msg, thread=thread)
    res = response(mensaje_estructurado)
    return res
