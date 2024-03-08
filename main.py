from fastapi import FastAPI
from dataBot import data
from models.structureMsg import strucMsg
from response import response
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
load_dotenv()
URLAuth = os.getenv('URLAUTHENTIC')
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["https://cotizador-frontend.vercel.app/","http://localhost:5173/"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


@app.get('/')
def root():
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
