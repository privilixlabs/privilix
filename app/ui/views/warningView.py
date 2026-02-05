import discord
from app.services.database.queries import edit_modlogs, delete_modlogs
from datetime import datetime
from app.core.constants.colors import BLUE


class WarningViewer(discord.ui.View):
    def __init__(self, warnings, target: discord.Member):
        super().__init__(timeout=120)
        self.warnings = warnings
        self.target = target
        self.index = 0
        self.update_buttons()

    def format_datetime(self, iso_str: str):
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%d %b %Y • %I:%M %p UTC")

    def get_embed(self):
        warn = self.warnings[self.index]

        embed = discord.Embed(title=f"Warnings for {self.target}", color=BLUE)

        embed.set_thumbnail(url=self.target.display_avatar.url)

        embed.add_field(name="Case ID", value=str(warn["id"]), inline=False)

        embed.add_field(name="Reason", value=warn["reason"], inline=False)

        embed.add_field(name="Moderator", value=f"<@{warn['moderator']}>", inline=True)

        embed.add_field(name="Resolved", value="Yes" if warn["resolved"] else "No")

        embed.add_field(
            name="Issued", value=self.format_datetime(warn["date"]), inline=True
        )

        embed.set_footer(text=f"Page ({self.index + 1}/{len(self.warnings)})")

        return embed

    def update_buttons(self):
        self.prev_btn.disabled = self.index == 0
        self.next_btn.disabled = self.index == len(self.warnings) - 1

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary)
    async def prev_btn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.index = max(0, self.index - 1)
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary)
    async def next_btn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.index = min(len(self.warnings) - 1, self.index + 1)
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.primary)
    async def edit_btn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        warn_id = self.warnings[self.index]["id"]

        class EditModal(discord.ui.Modal, title="Edit Warning"):
            new_reason = discord.ui.TextInput(
                label="New Reason", style=discord.TextStyle.paragraph
            )

            async def on_submit(self2, modal_interaction: discord.Interaction):
                try:
                    await edit_modlogs(warn_id, self2.new_reason.value)
                except Exception as e:
                    logger.error(e)
                self.warnings[self.index]["reason"] = self2.new_reason.value

                await modal_interaction.response.edit_message(
                    embed=self.get_embed(), view=self
                )

        await interaction.response.send_modal(EditModal())

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger)
    async def delete_btn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        warn_id = self.warnings[self.index]["id"]
        await delete_modlogs(warn_id)

        del self.warnings[self.index]

        if not self.warnings:
            return await interaction.response.edit_message(
                embed=discord.Embed(title="No warnings left.", color=BLUE),
                view=None,
            )

        self.index = max(0, self.index - 1)
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)
