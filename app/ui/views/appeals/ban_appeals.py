import discord
from discord import ui
from app.core.constants.colors import GREEN, RED
from app.core.constants.emojis import CHECK, CROSS
from app.ui.embeds import error_embed, success_embed
from app.services.database.queries import resolve_case


class BanAppealView(ui.View):
    def __init__(self, bot, target_id: int, case_id: int):
        super().__init__(timeout=None)
        self.bot = bot
        self.target_id = target_id
        self.case_id = case_id

    # def disable_all(self):
    #     for child in self.children:
    #         child.disabled = True

    @ui.button(label="Approve", style=discord.ButtonStyle.success)
    async def _unbanbtn(self, interaction: discord.Interaction, button: ui.Button):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message(
                embed=error_embed(
                    "You don’t have the required privileges to take this action."
                ),
                ephemeral=True,
            )
            return

        guild = interaction.guild
        target = await self.bot.fetch_user(self.target_id)
        if not guild:
            await interaction.response.send_message(
                embed=error_embed("Guild not found."), ephemeral=True
            )
            return

        try:
            target = await self.bot.fetch_user(self.target_id)
            await guild.unban(target, reason=f"Appeal accepted by {interaction.user}")
            await resolve_case(self.case_id)
        except Exception:
            await interaction.response.send_message(
                embed=error_embed("Failed to unban user."), ephemeral=True
            )
            return

        await interaction.response.send_message(
            embed=success_embed("Appeal accepted & user unbanned."), ephemeral=True
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
            dm = success_embed(
                "Your appeal has been accepted and you have been unbanned."
            )
            dm.title = f"{CHECK} Appeal Accepted"
            dm.set_footer(text=f"Sent from {guild.name}")
            await target.send(embed=dm)
        except:
            pass

    @ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def _declinebtn(self, interaction: discord.Interaction, button: ui.Button):
        if not interaction.user.guild_permissions.ban_members:
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
        target = await self.bot.fetch_user(self.target_id)
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
            dm = error_embed("Your appeal has been rejected and you remain banned.")
            dm.title = f"{CROSS} Appeal Declined"
            dm.set_footer(text=f"Sent from {interaction.guild.name}")
            await target.send(embed=dm)
        except:
            pass
