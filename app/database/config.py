from app.core.config import config


TORTOISE_ORM = {
    "connections": {"default": config.db_url},
    "apps": {
        "models": {
            "models": [
                "app.services.database.models.guild",
                "app.services.database.models.guild_settings",
                "app.services.database.models.mod_logs",
                "app.services.database.models.feature_settings",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}
