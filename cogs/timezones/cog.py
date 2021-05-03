import config
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
from utils.embedder import error_embed

from . import timezones


class Timezones(commands.Cog, name="⏲️ Timezones"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="to_utc",
        description=("Convert a date/time to UTC"),
        guild_ids=[config.GUILD_ID],
        options=[
            create_option(
                name="time",
                description="Date or time including timezone (eg. '5/29 1am -0500', '29 May 17:00 EST')",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            )
        ],
    )
    async def to_utc_slash(self, ctx: SlashContext, time: str):
        """Slash command: Convert a time from your timezone to UTC time."""
        await ctx.defer()
        await timezones.to_utc(ctx, time)

    @commands.command(aliases=["toUTC", "toutc", "utc", "to"])
    async def to_utc(self, ctx: commands.Context, *args):
        """Convert a time from your timezone to UTC time
        ```
        w!toUTC 5/29 13:00 IST
        ```
        """
        await timezones.to_utc(ctx, " ".join(args))

    @cog_ext.cog_slash(
        name="from_utc",
        description=("Convert a date/time to your timezone from UTC"),
        guild_ids=[config.GUILD_ID],
        options=[
            create_option(
                name="utc_time",
                description="UTC date or time to convert (eg. 29 May 3am)",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            ),
            create_option(
                name="to",
                description="Timezone that you want to convert to (eg. '-0500', 'EST')",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            ),
        ],
    )
    async def from_utc_slash(self, ctx: SlashContext, utc_time: str, to: str):
        """Slash command: Convert a time from your timezone to UTC time."""
        await ctx.defer()
        await timezones.from_utc(ctx, utc_time, to)

    @commands.command(aliases=["fromUTC", "fromutc", "from"])
    async def from_utc(self, ctx: commands.Context, *args: str):
        """Convert a time from your timezone to UTC time
        ```
        w!fromUTC 5/29 13:00 to MST
        ```
        """
        try:
            [utc_time, to] = " ".join(args).split(" to ", 1)
            await timezones.from_utc(ctx, utc_time, to)
        except ValueError:
            # unable to split date
            embed = error_embed(
                f"Sorry {ctx.author.name}, I didn't understand that.",
                "Make sure to include a date and target timezone. Use `w!help fromUTC` for more info.",
            )
            await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Timezones(bot))
