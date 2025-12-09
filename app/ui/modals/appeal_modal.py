import discord
from discord import ui, TextStyle
from app.services.database.queries import get_appeal_channel
from app.ui.embeds import error_embed, success_embed
from app.core.constants.colors import BLUE
from app.core.constants.emojis import HAMMER
from datetime import datetime
from app.ui.views.appeals.ban_appeals import BanAppealView
from app.ui.views.appeals.warn_appeals import WarnAppealView
from app.helpers.logging import logger


class Appeal(ui.Modal, title="Appeal Action"):
    def __init__(self, bot, guild_id: int, case_id: int, action: str):
        super().__init__()
        self.bot = bot
        self.guild_id = guild_id
        self.case_id = case_id
        self.action = action

        self.case_reason = ui.TextInput(
            label=(
                "Why were you banned?"
                if self.action == "ban"
                else "Why were you warned?"
            ),
            placeholder="Answer in a short sentence",
            style=TextStyle.short,
            required=True,
            max_length=200,
        )

        self.resolve_reason = ui.TextInput(
            label=(
                "Why should we unban you?"
                if self.action == "ban"
                else "Why should we remove your warning?"
            ),
            placeholder="Answer",
            style=TextStyle.paragraph,
            required=True,
            max_length=4000,
        )
        self.add_item(self.case_reason)
        self.add_item(self.resolve_reason)

    async def on_submit(self, interaction: discord.Interaction):
        channelid = await get_appeal_channel(self.guild_id)
        if not channelid:
            await interaction.response.send_message(
                embed=error_embed("This server has no appeals channel"), ephemeral=True
            )
            return
        channel = await self.bot.fetch_channel(int(channelid))
        view = (
            BanAppealView(self.bot, interaction.user.id, self.case_id)
            if self.action == "ban"
            else WarnAppealView(self.bot, interaction.user.id, self.case_id)
        )
        embed = discord.Embed(
            color=BLUE,
            title=f"{HAMMER} New {self.action.capitalize()} Appeal Submitted",
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.add_field(
            name="User", value=f"{interaction.user} (`{interaction.user.id}`)"
        )
        embed.add_field(
            name=(
                "Why were you banned?"
                if self.action == "ban"
                else "Why were you warned?"
            ),
            value=f"> {self.case_reason.value}",
        )
        embed.add_field(
            name=(
                "Why should we unban you?"
                if self.action == "ban"
                else "Why should we remove your warning?"
            ),
            value=f"> {self.resolve_reason.value}",
        )
        embed.set_footer(text=f"Submitted {datetime.now().strftime('today at %H:%M')}")

        try:
            await channel.send(embed=embed, view=view)
            await interaction.response.send_message(
                embed=success_embed("Your appeal has been submitted"), ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                embed=error_embed("Something went wrong"), ephemeral=True
            )
            logger.error(e)
