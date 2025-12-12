import discord
from discord import ui
from app.core.constants.emojis import HAMMER, BOX, STAR, SHIELD, GEAR
from app.core.constants.colors import BLUE

EMOJIS = {
    "Moderation": "🛡️",
    "Misc": "📦",
    "General": "⭐",
    "Management": "🔨",
    "Admin": "⚙️",
    "Fun": "🎭"
}

DESCRIPTIONS = {
    "Moderation": "Commands for managing members and server behavior.",
    "Misc": "Commands that don’t belong to any specific category.",
    "General": "Commands for everyday utility.",
    "Management": "Server management and utilities.",
    "Admin": "Commands for managing server settings and high-level controls.",
    "Fun": "Commands for fun."
}


class HelpView(ui.View):
    def __init__(self, bot, prefix):
        super().__init__(timeout=120)
        self.bot = bot
        self.prefix = prefix
        self.add_item(HelpSelect(bot, prefix))
        self.add_item(
            ui.Button(
                label="Invite",
                style=discord.ButtonStyle.link,
                url="https://discord.com/oauth2/authorize?client_id=1133741199505760266&permissions=8&integration_type=0&scope=bot",
            )
        )
        self.add_item(
            ui.Button(
                label="Support Server",
                style=discord.ButtonStyle.link,
                url="https://discord.gg/K6EDkaVERk",
            )
        )


class HelpSelect(ui.Select):
    def __init__(self, bot, prefix):
        self.bot = bot
        self.prefix = prefix
        options = [
            discord.SelectOption(
                label="Home",
                description="Return to the main help menu.",
                emoji="🏠",
            )
        ]

        for cog_name, cog in bot.cogs.items():
            if cog_name.lower() in [
                "connection",
                "join",
                "leave",
                "error",
                "load",
                "hi",
                "owner",
                "topgg"
            ]:
                continue

            options.append(
                discord.SelectOption(
                    label=cog_name,
                    emoji=EMOJIS.get(cog_name, "📁"),
                    description=DESCRIPTIONS.get(cog_name, f"Commands for {cog_name}."),
                )
            )

        super().__init__(
            placeholder="Select a category",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        selection = self.values[0]

        if selection == "Home":
            embed = discord.Embed(
                title="📚 Help Menu",
                description=f"> Use `{self.prefix}help <command>` to show information about a command.",
                color=BLUE,
            )
            embed.set_footer(text="Pick a category to browse available commands")
            return await interaction.response.edit_message(
                embed=embed, view=HelpView(self.bot, self.prefix)
            )

        cog = self.bot.get_cog(selection)

        embed = discord.Embed(
            title=f"{EMOJIS.get(selection)} {selection} Commands",
            description=f"-# {DESCRIPTIONS.get(selection)}",
            color=BLUE,
        )

        for cmd in cog.get_commands():
            if not cmd.hidden:
                embed.add_field(
                    name=f"`{self.prefix}{cmd.name}`",
                    value=cmd.help or "No description provided.",
                    inline=False,
                )

        await interaction.response.edit_message(embed=embed, view=HelpView(self.bot, self.prefix))
