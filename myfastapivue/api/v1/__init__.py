from fastapi import APIRouter
from .endpoints import *
v1=APIRouter(prefix="")
v1.include_router(weatherApp)
v1.include_router(translationApp)
v1.include_router(lolApp)