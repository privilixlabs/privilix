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

    @app_commands.command(name="invite", description="Get an invite link for Privilix.")
    @app_commands.guild_only()
    async def _inviteslash(self, interaction: discord.Interaction):
        view = ui.View()
        link_btn = ui.Button(
            label="Invite",
            style=discord.ButtonStyle.link,
            url="https://discord.com/oauth2/authorize?client_id=1133741199505760266&permissions=8&integration_type=0&scope=bot",
        )
        view.add_item(link_btn)
        embed = discord.Embed(
            color=BLUE,
            title="Thanks for your interest in Privilix!",
            description="> Click the button to invite the bot to your server!",
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(
            text=f"Requested by {interaction.user.name} | {datetime.now().strftime('Today at %H:%M')}",
            icon_url=interaction.user.display_avatar.url,
        )
        
        await interaction.response.send_message(embed = embed, view = view)

async def setup(bot):
    await bot.add_cog(Hi(bot))
