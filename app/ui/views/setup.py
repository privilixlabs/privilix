import discord
from discord import ui

from app.core.constants.colors import BLUE
from app.services.database.queries import (
    set_modlog_channel,
    set_appeal_channel,
)

from datetime import datetime


class Setup(ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=300)

    @ui.button(label="Start Setup", style=discord.ButtonStyle.green, emoji="🚀")
    async def start_btn(self, interaction: discord.Interaction, button: ui.Button):
        self.clear_items()
        self.add_item(ModlogSelect(self.bot))
        embed = discord.Embed(
            title="Setup • Mod Logs",
            description="Select a channel where moderation logs should be sent.",
            color=BLUE,
        )

        await interaction.response.edit_message(embed=embed, view=self)


class ModlogSelect(ui.ChannelSelect):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(
            placeholder="Select a mod logs channel",
            channel_types=[discord.ChannelType.text],
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        channel = self.values[0]

        await set_modlog_channel(interaction.guild.id, channel.id)
        self.bot.guild_settings_cache[interaction.guild.id]["modlogs_channelid"] = (
            channel.id
        )

        embed = interaction.message.embeds[0]
        setup = Setup(self.bot)
        setup.clear_items()
        setup.add_item(AppealSelect(self.bot))
        embed = discord.Embed(
            title="Setup • Appeals",
            description="Select a channel where appeals should be sent.",
            color=BLUE,
        )

        await interaction.followup.edit_message(
            message_id=interaction.message.id, embed=embed, view=setup
        )


class AppealSelect(ui.ChannelSelect):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(
            placeholder="Select an appeals channel",
            channel_types=[discord.ChannelType.text],
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        channel = self.values[0]

        await set_appeal_channel(interaction.guild.id, channel.id)
        self.bot.guild_settings_cache[interaction.guild.id]["appeals_channelid"] = (
            channel.id
        )

        embed = interaction.message.embeds[0]
        embed = discord.Embed(
            color=BLUE,
            title="Quick Setup Completed",
            description=f"{interaction.user.mention} completed the quick setup",
        )
        modlog_channel = interaction.guild.get_channel(
            self.bot.guild_settings_cache[interaction.guild.id]["modlogs_channelid"]
        )
        appeal_channel = interaction.guild.get_channel(
            self.bot.guild_settings_cache[interaction.guild.id]["appeals_channelid"]
        )
        embed.add_field(
            name="Setup information",
            value=f"> **Mod Logs channel**: {modlog_channel.mention}\n> **Appeals channel**: {appeal_channel.mention}",
        )
        embed.set_footer(text=datetime.now().strftime("Today at %H:%M"))

        await interaction.followup.edit_message(
            message_id=interaction.message.id, embed=embed, view=None
        )
