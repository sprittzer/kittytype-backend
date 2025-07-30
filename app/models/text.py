from tortoise import fields
from tortoise.models import Model
from typing import Optional

class Text(Model):
    id = fields.IntField(primary_key=True)
    body = fields.TextField()
    language = fields.CharField(max_length=10, default="en")
    
    mode = fields.CharField(max_length=20)  # "time", "words", "quote", "zen"
    
    punctuation = fields.BooleanField(default=False)  # включены ли знаки препинания
    numbers = fields.BooleanField(default=False)      # включены ли цифры
    
    length = fields.IntField(null=True)
    
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "texts"