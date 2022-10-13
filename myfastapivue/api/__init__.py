from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise


from .v1 import v1


app=FastAPI(title="天气预报API",description="天气预报API",version="1.0.0")

app.include_router(v1,prefix="/v1")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)