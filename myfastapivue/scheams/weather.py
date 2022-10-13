from tortoise.contrib.pydantic import pydantic_model_creator

from models import Weather

Weather_Pydantic = pydantic_model_creator(Weather, name="Weather")
WeatherIn_Pydantic = pydantic_model_creator(Weather, name="WeatherIn", exclude_readonly=True)