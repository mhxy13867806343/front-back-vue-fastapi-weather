from tortoise import models
from tortoise import fields


class Translation(models.Model):
    name = fields.CharField(max_length=50, null=False, description="字典名称")
    code = fields.CharField(max_length=50, null=False, description="字典编码")
    value = fields.CharField(max_length=50, null=False, description="字典值")
