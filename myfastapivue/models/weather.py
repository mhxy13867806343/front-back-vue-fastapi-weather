from tortoise import models
from tortoise import fields


class Weather(models.Model):
    name = fields.CharField(max_length=50, null=False, description="天气名称")
    adcode = fields.CharField(max_length=50, null=False, description="天气编码")
    citycode = fields.CharField(max_length=50, null=False, description="城市编码")
