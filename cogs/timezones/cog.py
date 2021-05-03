import config
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

from . import timezones


class Timezones(commands.Cog, name="⏲️ Timezones"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="to_utc",
        description=("Convert a date/time to UTC."),
        guild_ids=[config.GUILD_ID],
        options=[
            create_option(
                name="time",
                description="Date or time to convert including the time zone",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            )
        ],
    )
    async def to_utc_slash(self, ctx: SlashContext, time: str):
        """Slash command: Convert a time from your timezone to UTC time."""
        await timezones.to_utc(ctx, time)

    @commands.command(aliases=["toUTC", "toutc", "utc"])
    async def to_utc(self, ctx: commands.Context, *args):
        """Convert a time from your timezone to UTC time
        ```
        w!toUTC 5/29 13:00 IST
        ```
        """
        await timezones.to_utc(ctx, args.join(" "))


def setup(bot: commands.Bot):
    bot.add_cog(Timezones(bot))
