from tortoise.contrib.pydantic import pydantic_model_creator

from models import Translation

Translation_Pydantic = pydantic_model_creator(Translation, name="Translation")
TranslationIn_Pydantic = pydantic_model_creator(Translation, name="TranslationIn", exclude_readonly=True)