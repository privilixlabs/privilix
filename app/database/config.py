from app.core.config import config


TORTOISE_ORM = {
    "connections": {"default": config.db_url},
    "apps": {
        "models": {
            "models": [
                "app.database.models.guild",
                "app.database.models.guild_settings",
                "app.database.models.mod_logs",
                "app.database.models.feature_settings",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}
