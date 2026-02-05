import discord
from discord.ext import commands


class Mention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == f"<@{self.bot.user.id}>":
            await message.channel.send(
                f"Hello {message.author.mention}! Try `/help` for more info!"
            )


async def setup(bot):
    await bot.add_cog(Mention(bot))
