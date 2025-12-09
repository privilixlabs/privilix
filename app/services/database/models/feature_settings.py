from tortoise import models, fields
from .guild import Guild


class FeatureSettings(models.Model):
    guild: Guild = fields.OneToOneField(
        "models.Guild", related_name="features", pk=True, on_delete=fields.CASCADE
    )
    suggestions = fields.BooleanField(default=False)
    modlogs = fields.BooleanField(default=False)
    appeals = fields.BooleanField(default=False)

    class Meta:
        table = "feature_settings"
