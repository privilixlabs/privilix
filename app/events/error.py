import discord
from discord.ext import commands
from app.helpers.logging import logger
from app.ui.embeds import error_embed
from app.core.constants.emojis import CROSS, LOADER


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            await ctx._loading_message.remove_reaction(LOADER, self.bot.user)
        except Exception as e:
            logger.error(f"Remove reaction on command error failed: {e}")

        if hasattr(ctx.command, "on_error"):
            return

        bad = (
            commands.BadArgument,
            commands.MissingRequiredArgument,
            commands.TooManyArguments,
            commands.UserInputError,
        )

        if isinstance(error, bad):
            params = []
            for name, param in ctx.command.clean_params.items():
                if param.default is param.empty:
                    params.append(f"<{name}>")
                else:
                    params.append(f"[{name}]")

            usage = f"> `.{ctx.command.name} {' '.join(params)}`"

            embed = error_embed(title=f"{CROSS} Wrong Usage")
            embed.add_field(name="Usage", value=usage)

            await ctx.reply(embed=embed, mention_author=False)
            return

        if isinstance(error, commands.MissingPermissions):
            embed = error_embed(
                "You don’t have the required privileges to use this command.",
                title=f"{CROSS} Permission Denied",
            )
            await ctx.reply(embed=embed, mention_author=False)
            return

        raise error


async def setup(bot):
    await bot.add_cog(Error(bot))
