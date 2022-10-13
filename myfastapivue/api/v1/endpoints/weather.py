from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel
from models import Weather
from getAjax import getWeatherData
# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///weather.sqlite"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

weather = sqlalchemy.Table(
    "weather",
    metadata,
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("adcode", sqlalchemy.String),
    sqlalchemy.Column("citycode", sqlalchemy.String),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


weatherApp= APIRouter(tags=["天气相关接口"])

#获取所有天气地区
@weatherApp.get("/list")
async def get_list():
    query = weather.select()
    data=[]
    querys=await database.fetch_all(query)
    for i in querys:
            data.append({
                "name": i[0],
                "adcode": i[1],
                "citycode": i[2]
            })
    return {
        "msg": "获取成功",
        "data": data,
        "total":len(data),
        "code": 200
    }
# 通过城市名称获取城市天气
@weatherApp.get('/weatherDetails')
async def get_weatherDetails(name:str):
    query = weather.select().where(weather.c.name==name)
    querys = await database.fetch_all(query)
    data = {
            "name": querys[0][0],
            "adcode": querys[0][1],
            "citycode": querys[0][2]
        }
    return {
        "msg": "获取成功",
        "data": data,
        "code": 200
    }
#模糊查询
@weatherApp.get("/weather")
async def get_weather(name:str):
    data=[]
    query = weather.select().filter(weather.c.name.like('%' + name + '%'))
    # print(dir(weather.c.name.like(search+'%')))
    querys = await database.fetch_all(query)

    # if(len(querys)==0):
    #     query = weather.select()
    #     querys= await database.fetch_all(query)
    #     for i in querys:
    #         data.append({
    #             "name": i[0],
    #             "adcode": i[1],
    #             "citycode": i[2]
    #         })
    if (len(querys) == 1):
        data =[
            {
                "name": querys[0][0],
                "adcode": querys[0][1],
                "citycode": querys[0][2]
            }
        ]
    elif len(querys) > 1:
        for i in querys:
            data.append({
                "name": i[0],
                "adcode": i[1],
                "citycode": i[2]
            })
    return {
        "msg": "获取成功",
        "data": data,
        "code": 200
    }
#根据详情查询高德真正的数据
@weatherApp.get("/gdWeather",description="根据详情查询高德真正的数据")
async def get_weather(code:str='330100'):
    data=getWeatherData(code)
    return {
        "msg": "获取成功",
        "data": data,
        "code": 200
    }

__all__ = ['weather']