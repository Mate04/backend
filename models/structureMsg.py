from pydantic import BaseModel

class strucMsg(BaseModel):
    msg:str
    thread:str = None