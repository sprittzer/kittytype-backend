from tortoise import fields
from tortoise.models import Model

class PerformanceLog(Model):
    id = fields.IntField(pk=True)
    game = fields.ForeignKeyField("models.Game", related_name="performance_logs")
    user = fields.ForeignKeyField("models.User", related_name="performance_logs")

    second = fields.IntField()
    wpm = fields.FloatField()
    raw_wpm = fields.FloatField()
    errors = fields.IntField()

    class Meta:
        table = "performance_logs"
        unique_together = ("game", "second")
