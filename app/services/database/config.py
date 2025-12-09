TORTOISE_ORM = {
    "connections": {"default": f"sqlite://data/database.db"},
    "apps": {
        "models": {
            "models": [
                "app.services.database.models.guild",
                "app.services.database.models.guild_settings",
                "app.services.database.models.mod_logs",
                "app.services.database.models.feature_settings",
                "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}