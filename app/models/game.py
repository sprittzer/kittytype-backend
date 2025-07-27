from tortoise import fields
from tortoise.models import Model

class Game(Model):
    id = fields.IntField(pk=True)
    
    user = fields.ForeignKeyField(
        "models.User", related_name="games"
    )
    
    text = fields.ForeignKeyField(
        "models.Text", related_name="games"
    )
    
    wpm = fields.FloatField()
    raw_wpm = fields.FloatField()
    accuracy = fields.FloatField()
    errors = fields.IntField()
    duration = fields.IntField()
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "games"
