from tortoise import models, fields
from .guild import Guild


class GuildSettings(models.Model):
    guild: Guild = fields.OneToOneField(
        "models.Guild", related_name="settings", pk=True, on_delete=fields.CASCADE
    )
    prefix = fields.CharField(max_length=5, default=".")
    language = fields.CharField(max_length=10, default="en")
    modlog_channelid = fields.CharField(max_length=32, null=True)
    suggestion_channelid = fields.CharField(max_length=32, null=True)
    appeal_channelid = fields.CharField(max_length=32, null=True)

    class Meta:
        table = "guild_settings"
