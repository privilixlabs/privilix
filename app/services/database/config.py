import os
from dotenv import load_dotenv
load_dotenv()


TORTOISE_ORM = {
    "connections": {"default": os.getenv('DB_URL')},
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