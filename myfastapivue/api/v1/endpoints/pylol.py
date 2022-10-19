
from typing import List

import databases
import sqlalchemy
from fastapi import APIRouter, Depends,FastAPI
from pydantic import BaseModel
import requests
import json
DATABASE_URL = "sqlite:///dblol.sqlite"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
url='https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js?ts=2776676'
data=requests.get(url)
content=bytes(data.content).decode('UTF-8')
jsonContent=json.loads(content)
fileName=jsonContent['fileName']
fileTime=jsonContent['fileTime']
hero=jsonContent['hero']
version=jsonContent['version']
lol = sqlalchemy.Table(
    "lol",
    metadata,
    sqlalchemy.Column("fileName", sqlalchemy.String),
    sqlalchemy.Column("fileTime", sqlalchemy.String),
    sqlalchemy.Column("hero", sqlalchemy.String),
    sqlalchemy.Column("version", sqlalchemy.String),
)
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

metadata.create_all(engine)
class LolIn(BaseModel):
    fileName: str
    fileTime: str
    hero: str
    version: str
class LolData(BaseModel):
    fileName: str
    fileTime: str
    hero: str
    version: str

lolApp =APIRouter(tags=["lol英雄接口相关"])

@lolApp.on_event("startup")
async def startup():
    await database.connect()
@lolApp.on_event("shutdown")
async def shutdown():
    await database.disconnect()
@lolApp.get("/lol",response_model=List[LolData])
async def get_lol():
    query = lol.select()
    return await database.fetch_all(query)