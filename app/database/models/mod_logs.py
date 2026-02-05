from tortoise import models, fields
from .guild import Guild


class ModLogs(models.Model):
    case_id = fields.IntField(pk=True)
    guild: Guild = fields.ForeignKeyField(
        "models.Guild", related_names="logs", on_delete=fields.CASCADE
    )
    target_id = fields.CharField(max_length=32)
    mod_id = fields.CharField(max_length=32)
    action = fields.CharField(max_length=20)
    reason = fields.TextField()
    timestamp = fields.DatetimeField(auto_now_add=True)
    resolved = fields.BooleanField(default=False)

    class Meta:
        table = "mod_logs"
