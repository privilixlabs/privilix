import discord
from discord import ui

from app.ui.embeds import error_embed, success_embed
from app.services.database.queries import resolve_case
from app.core.constants.colors import GREEN, RED
from app.core.constants.emojis import CHECK, CROSS


class WarnAppealView(ui.View):
    def __init__(self, bot, target_id: int, case_id: int):
        super().__init__()
        self.bot = bot
        self.target_id = target_id
        self.case_id = case_id

    @ui.button(label="Approve", style=discord.ButtonStyle.success)
    async def approvebtn(self, interaction: discord.Interaction, button: ui.Button):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                embed=error_embed(
                    "You don’t have the required privileges to take this action."
                ),
                ephemeral=True,
            )
            return

        try:
            await resolve_case(self.case_id)
        except Exception as e:
            await interaction.response.send_message(
                embed=error_embed("Failed to close warning."), ephemeral=True
            )
            return

        guild = interaction.guild

        await interaction.response.send_message(
            embed=success_embed("Appeal accepted & warning closed."), ephemeral=True
        )

        if interaction.message:
            embed = interaction.message.embeds[0]
            embed.color = GREEN
            embed.title = f"{CHECK} Appeal Accepted"
            embed.add_field(
                name="Status",
                value=f"Accepted by {interaction.user.mention}",
                inline=False,
            )
            # self.disable_all()
            await interaction.message.edit(embed=embed, view=None)

        try:
            target = await self.bot.fetch_user(self.target_id)
            dm = success_embed(
                "Your appeal has been accepted and your warning has been closed."
            )
            dm.title = f"{CHECK} Appeal Accepted"
            dm.set_footer(text=f"Sent from {guild.name}")
            await target.send(embed=dm)
        except:
            pass

    @ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def declinebtn(self, interaction: discord.Interaction, button: ui.Button):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                embed=error_embed(
                    "You don’t have the required privileges to take this action."
                ),
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            embed=success_embed("Appeal declined."), ephemeral=True
        )

        if interaction.message:
            embed = interaction.message.embeds[0]
            embed.color = RED
            embed.title = f"{CROSS} Appeal Declined"
            embed.add_field(
                name="Status",
                value=f"Declined by {interaction.user.mention}",
                inline=False,
            )
            # self.disable_all()
            await interaction.message.edit(embed=embed, view=None)

        try:
            target = await self.bot.fetch_user(self.target_id)
            dm = error_embed("Your warn appeal has been declined.")
            dm.title = f"{CROSS} Appeal Declined"
            dm.set_footer(text=f"Sent from {interaction.guild.name}")
            await target.send(embed=dm)
        except:
            pass
