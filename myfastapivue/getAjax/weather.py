import requests
import json
gdKey = '44e6ffc37402f6e509d801400917e333'
host='https://restapi.amap.com/v3/weather/weatherInfo'

def getWeatherData(city='330100'):
    url = f"{host}?key={gdKey}&city={city}&extensions=all"
    res = requests.get(url)
    data=res.json()
    if data['status']=='0':
        return {"msg":data['info'],"code":6002}
    return res.json()