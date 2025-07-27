from tortoise import fields
from tortoise.models import Model

class Text(Model):
    id = fields.IntField(primary_key=True)
    body = fields.TextField()
    language = fields.CharField(max_length=10, default="en")
    mode = fields.CharField(max_length=20)  # "time", "words", "quote"
    length = fields.IntField(null=True)  # количество слов/секунд  
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "texts"