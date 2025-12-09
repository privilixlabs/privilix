import os
import asyncio
from dotenv import load_dotenv
from app.core.bot import Privilix
from tortoise import Tortoise
from app.services.database.config import TORTOISE_ORM
from app.helpers.logging import logger

async def init_db():
  await Tortoise.init(config = TORTOISE_ORM)


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Bot token missing in .env")

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
