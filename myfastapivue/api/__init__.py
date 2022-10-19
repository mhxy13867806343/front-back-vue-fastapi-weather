from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise


from .v1 import v1


app=FastAPI(title="学习python的前后端分离进行使用的API",description="前后端分离进行使用API",version="1.0.1")

app.include_router(v1,prefix="/v1")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)