from fastapi import FastAPI
from dataBot import data
from models.structureMsg import strucMsg
from response import response
app = FastAPI()

@app.get('/')
def root():
    return 
@app.post('/')
def root(strucMsg:strucMsg):
    return response(strucMsg)
@app.get('/getData')
def dataBot():
    return data()
