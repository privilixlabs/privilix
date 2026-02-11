import discord
from discord.ext import commands
from app.helpers.logging import logger
from app.database.models.guild_settings import GuildSettings


class Privilix(commands.Bot):
    def __init__(self, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True

        allowed_mentions = discord.AllowedMentions(replied_user=False)

        super().__init__(
            command_prefix=get_prefix,
            intents=intents,
            help_command=None,
            allowed_mentions=allowed_mentions,
            **kwargs,
        )

        self.prefix_cache: dict[int, str] = {}
        self.guild_settings_cache: dict[int, dict] = {}

    async def setup_hook(self):
        rows = await GuildSettings.all().prefetch_related("guild")
        for row in rows:
            guild_id = int(row.guild.guild_id)
            self.prefix_cache[guild_id] = row.prefix
            self.guild_settings_cache[guild_id] = {
                "language": row.language,
                "modlogs_channelid": row.modlog_channelid,
                "suggestion_channelid": row.suggestion_channelid,
                "appeals_channelid": row.appeal_channelid,
            }
        logger.info(f"Cached {len(self.prefix_cache)} guild configs")

    async def load_all_extensions(self):
        import os

        folders = ["app/commands", "app/events", "app/tasks"]

        for folder in folders:
            for file in os.listdir(folder):
                if file.endswith(".py") and file != "__init__.py":
                    path = file[:-3]
                    extension = f"{folder.replace('/', '.')}.{path}"

                    try:
                        await self.load_extension(extension)
                        logger.info(f"Loaded extension : {path}")
                    except Exception as e:
                        logger.error(f"Failed to load {path} : {e}")


async def get_prefix(bot: Privilix, message: discord.Message):
    assert message.guild is not None
    pref = bot.prefix_cache.get(message.guild.id, ".")
    return commands.when_mentioned_or(pref)(bot, message)
