import discord
from datetime import datetime
from app.services.database.queries import delete_modlogs, edit_modlogs
from app.core.constants.colors import BLUE


class Modlogs(discord.ui.View):
    def __init__(self, modlogs, target: discord.Member):
        super().__init__(timeout=120)
        self.modlogs = modlogs
        self.target = target
        self.index = 0
        self.update_buttons()

    def format_datetime(self, iso_str: str):
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%d %b %Y • %I:%M %p UTC")

    def get_embed(self):
        log = self.modlogs[self.index]

        embed = discord.Embed(title=f"Modlogs for {self.target}", color=BLUE)

        embed.set_thumbnail(url=self.target.display_avatar.url)

        embed.add_field(name="Case ID", value=str(log["id"]), inline=False)

        embed.add_field(name="Action", value=log["action"], inline=False)

        embed.add_field(name="Reason", value=log["reason"], inline=False)

        embed.add_field(name="Moderator", value=f"<@{log['moderator']}>", inline=True)

        embed.add_field(name="Resolved", value="Yes" if log["resolved"] else "No")

        embed.add_field(
            name="Issued", value=self.format_datetime(log["date"]), inline=True
        )

        embed.set_footer(text=f"Page ({self.index + 1}/{len(self.modlogs)})")

        return embed

    def update_buttons(self):
        self.prev_btn.disabled = self.index == 0
        self.next_btn.disabled = self.index == len(self.modlogs) - 1

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
        self.index = min(len(self.modlogs) - 1, self.index + 1)
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.primary)
    async def edit_btn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        action_id = self.modlogs[self.index]["id"]

        class EditModal(discord.ui.Modal, title="Edit Log"):
            new_reason = discord.ui.TextInput(
                label="New Reason", style=discord.TextStyle.paragraph
            )

            async def on_submit(self2, modal_interaction: discord.Interaction):
                await edit_modlogs(action_id, self2.new_reason.value)
                self.modlogs[self.index]["reason"] = self2.new_reason.value

                await modal_interaction.response.edit_message(
                    embed=self.get_embed(), view=self
                )

        await interaction.response.send_modal(EditModal())

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger)
    async def delete_btn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        action_id = self.modlogs[self.index]["id"]
        await delete_modlogs(action_id)

        del self.modlogs[self.index]

        if not self.modlogs:
            return await interaction.response.edit_message(
                embed=discord.Embed(title="No logs left.", color=BLUE),
                view=None,
            )

        self.index = max(0, self.index - 1)
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)
