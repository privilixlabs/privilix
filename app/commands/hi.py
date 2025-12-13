import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from app.core.constants.colors import BLUE
from app.services.database.queries import fetch_prefix
from datetime import datetime


class Hi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="hi",
        description="""A quick onboarding message for new users.""",
    )
    async def _hi(self, interaction: discord.Interaction):
        pref = await fetch_prefix(interaction.guild.id)
        embed = discord.Embed(
            color=BLUE,
            description=f"""## Welcome to Privilix. \n-# Less Stress. More Community. \n--------------\n### Current Prefix: **`{pref}`**""",
        )
        embed.add_field(
            name="Quickstart",
            value=f"> Use `{pref}setprefix <prefix>` to change my prefix.\n> Use `{pref}help` to get a list of all my commands.",
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        now = datetime.now().strftime("Today at %H:%M")
        embed.set_footer(text=f"Privilix | {now}")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Hi(bot))
