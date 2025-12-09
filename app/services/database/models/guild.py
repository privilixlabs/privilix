from tortoise import models, fields


class Guild(models.Model):
    guild_id = fields.CharField(pk=True, max_length=32)
    name = fields.CharField(max_length=200)
    joined_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "guild"
