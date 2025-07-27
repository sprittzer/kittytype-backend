from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=64, unique=True)
    email = fields.CharField(max_length=320, unique=True)
    hashed_password = fields.CharField(max_length=255)
    
    # профиль
    bio = fields.TextField(null=True)
    keyboard = fields.CharField(max_length=128, null=True)
    longest_streak = fields.IntField(default=0)
    joined_date = fields.DatetimeField(auto_now_add=True)
    
    # текущее состояние
    current_streak = fields.IntField(default=0)
    theme = fields.CharField(max_length=64, default='dark')
    language = fields.CharField(max_length=10, default="en")
    
    
    class Meta:
        table = "users"