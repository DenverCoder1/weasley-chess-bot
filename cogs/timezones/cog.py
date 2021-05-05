import discord
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

    @cog_ext.cog_subcommand(
        base="to",
        name="utc",
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

    @cog_ext.cog_subcommand(
        base="from",
        name="utc",
        description=("Convert a date/time to your timezone from UTC"),
        guild_ids=[config.GUILD_ID],
        options=[
            create_option(
                name="time",
                description="UTC date or time to convert (eg. 29 May 3am)",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            ),
            create_option(
                name="timezone",
                description="Timezone that you want to convert to (eg. '-0500', 'EST')",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            ),
        ],
    )
    async def from_utc_slash(self, ctx: SlashContext, time: str, timezone: str):
        """Slash command: Convert a time from your timezone to UTC time."""
        await ctx.defer()
        await timezones.from_utc(ctx, time, timezone)

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

    @cog_ext.cog_subcommand(
        base="time",
        name="diff",
        description=("Get the amount of time until a date occurs"),
        guild_ids=[config.GUILD_ID],
        options=[
            create_option(
                name="time",
                description="Date or time to subtract (eg. 29 May 3am)",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            ),
            create_option(
                name="message",
                description="Message to include along with the time difference",
                option_type=SlashCommandOptionType.STRING,
                required=False,
            ),
        ],
    )
    async def time_diff_slash(self, ctx: SlashContext, time: str, message: str = ""):
        """Slash command: Find a time difference"""
        await ctx.defer()
        await timezones.time_diff(ctx, time, message)

    @commands.command(aliases=["timeDiff", "timediff", "diff", "time_until", "td"])
    async def time_diff(self, ctx: commands.Context, *args: str):
        """Find a time difference
        ```
        w!timeDiff 5/29 13:00
        w!timeDiff 5/29 13:00 "Message"
        ```
        """
        # use the last argument as a message to display if it's in quotes
        if ctx.message.content.find(f'"{args[-1]}"') > -1:
            return await timezones.time_diff(ctx, " ".join(args[:-1]), args[-1])
        # otherwise, use all of the arguments as the time
        await timezones.time_diff(ctx, " ".join(args))

    @cog_ext.cog_subcommand(
        base="tz",
        name="info",
        description=("Get information about a timezone"),
        guild_ids=[config.GUILD_ID],
        options=[
            create_option(
                name="timezone",
                description="Timezone abbreviation (eg. BST)",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            ),
        ],
    )
    async def tzinfo_slash(self, ctx: SlashContext, timezone: str = "UTC"):
        """Slash command: Find information about a timezone"""
        await ctx.defer()
        await timezones.send_tzinfo(ctx, timezone)

    @commands.command(aliases=["tzInfo", "timezone", "tz_info", "tz"])
    async def tzinfo(self, ctx: commands.Context, timezone: str):
        """Find information about a timezone
        ```
        w!tzinfo BST
        ```
        """
        await timezones.send_tzinfo(ctx, timezone)


def setup(bot: commands.Bot):
    bot.add_cog(Timezones(bot))
