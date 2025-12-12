import discord
from discord.ext import commands
import random


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball", description="Ask a question to the magic ball")
    async def _8ball(self, ctx: commands.context, *, question: str):
        answers = [
            "No",
            "Likely not",
            "Yes",
            "Ask your question again",
            "Very likely",
            "Impossible",
            "Without a doubt",
            "It's No",
            "Yes definitely",
        ]
        answer = random.randint(0, len(answers) - 1)

        ball = discord.Embed(color=0xA865B5, title="8ball 🔮")
        ball.add_field(name="Question", value=question)
        ball.add_field(name="Answer", value=answers[answer])

        await ctx.reply(embed=ball)


async def setup(bot):
  await bot.add_cog(Fun(bot))