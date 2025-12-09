import discord
from discord import ui
from app.ui.modals.appeal_modal import Appeal


class AppealDMView(ui.View):
    def __init__(self, bot, guild_id: int, case_id: int, action: str):
        super().__init__(timeout=None)
        self.bot = bot
        self.guild_id = guild_id
        self.case_id = case_id
        self.action = action

    @ui.button(label="Appeal", style=discord.ButtonStyle.primary)
    async def appeal_btn(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(
            Appeal(self.bot, self.guild_id, self.case_id, self.action)
        )
