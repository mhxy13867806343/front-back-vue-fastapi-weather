from fastapi import APIRouter, Depends




import json




translationApp= APIRouter(tags=["翻译相关接口"])
from getAjax import getTranslationConnect
@translationApp.post("/fy",description="翻译相关的接口")
async def posttranslation(q="",langType="",dicts=""):
    data = getTranslationConnect(q,langType,dicts)
    datatranlast=bytes(data).decode('UTF-8')
    utf8=json.loads(datatranlast)
    if(utf8['errorCode']=='0'):
        data={
            **utf8
        }
        return {
            "msg": "获取成功",
            "data":data,
            "code": 200
        }
    else:
        return {
            "msg": "获取失败",
            "data":{},
            "code":6002
        }
@translationApp.get("/fylanguage",description="支持语言的接口")
async def gettranslation():
    data=[
        {
            "name": "自动识别",
            "value": "auto"
        },
        {
            "name": "中文",
            "value": "zh-CNS"
        },
        {
            "name": "英文",
            "value": "en"
        },
        {
            "name": "日文",
            "value": "ja"
        },
        {
            "name": "韩文",
            "value": "ko"
        }

    ]
    return {
        "msg": "获取成功",
        "data": data,
        "code": 200
    }

@translationApp.get("/fydict",description="支持词典的接口")
async def gettranslation():
    data=[
        {
            "name": "汉语词典",
            "value": "yw",
            "code":"zh-CHS"
        },
        {
            "name": "英英词典",
            "value": "ee",
            "code": "en"
        },
        {
            "name": "汉英词典",
            "value": "ce",
            "code": "zh-CHS"
        },
        {
            "name": "英汉词典",
            "value": "ec",
            "code": "en"
        },
        {
            "name": "日中词典",
            "value": "jc",
            "code": "ja"
        },
        {
            "name": "中日词典",
            "value": "cj",
            "code": "zh-CHS"
        },
        {
            "name": "韩中词典",
            "value": "kc",
            "code": "ko"
        },
        {
            "name": "中韩词典",
            "value": "ck",
            "code": "zh-CHS"
        },
    ]
    return {
        "msg": "获取成功",
        "data": data,
        "code": 200
    }





