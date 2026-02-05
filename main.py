import asyncio
from app.core.bot import Privilix
from app.core.config import config
from tortoise import Tortoise
from app.services.database.config import TORTOISE_ORM


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)


TOKEN = config.bot_token

bot = Privilix()


async def main():
    async with bot:
        await init_db()
        await bot.load_all_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot shutdown requested.")
