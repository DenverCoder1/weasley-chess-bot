from datetime import datetime
from typing import Union

from discord.ext import commands
from discord_slash.context import SlashContext
from utils.dates import format_date, get_clock_emoji, parse_date
from utils.embedder import build_embed, error_embed
from utils.timestamps import Timestamp, TimestampFormat


async def to_utc(ctx: Union[commands.Context, SlashContext], date_input: str):
    # parse the date
    new_date = parse_date(date_input, to_tz="UTC")
    if isinstance(new_date, datetime) and parse_date(date_input).tzinfo:
        return await __send_time_embed(ctx, new_date, date_input)
    # unable to parse date
    embed = error_embed(
        f"Sorry {ctx.author.name}, I didn't understand that.",
        "Make sure to include a date and timezone. Use `w!help toUTC` for more info.",
    )
    await ctx.send(embed=embed)


async def from_utc(
    ctx: Union[commands.Context, SlashContext], date_str: str, to_tz: str
):
    new_date = parse_date(date_str, from_tz="UTC", to_tz=to_tz)
    if isinstance(new_date, datetime):
        date_input = date_str if "UTC" in date_str else f"{date_str} (UTC)"
        return await __send_time_embed(ctx, new_date, date_input, to_tz)
    # unable to parse date
    embed = error_embed(
        f"Sorry {ctx.author.name}, I didn't understand that.",
        "Make sure to include a date and timezone. Use `w!help fromUTC` for more info.",
    )
    await ctx.send(embed=embed)


async def time_diff(
    ctx: Union[commands.Context, SlashContext],
    date_input: str,
    message: str = "",
):
    new_date = parse_date(date_input, to_tz="UTC")
    if isinstance(new_date, datetime):
        return await __send_diff_embed(ctx, new_date, message)
    # unable to parse date
    embed = error_embed(
        f"Sorry {ctx.author.name}, I didn't understand that.",
        "Make sure to include a valid date. Use `w!help timeDiff` for more info.",
    )
    await ctx.send(embed=embed)


async def __send_time_embed(
    ctx: Union[commands.Context, SlashContext],
    date_output: datetime,
    date_input: str,
    timezone: str = "UTC",
):
    clock = get_clock_emoji(date_output)
    embed = build_embed(
        title=f"{clock} {format_date(date_output)} {timezone}",
        description=(f'Converted to {timezone} from "{date_input}"'),
    )
    await ctx.send(embed=embed)


async def __send_diff_embed(
    ctx: Union[commands.Context, SlashContext], date: datetime, message: str = ""
):
    description = f"**{message}**\n" if message else ""
    description += Timestamp(date).format(TimestampFormat.RELATIVE_TIME)
    clock = get_clock_emoji(date)
    embed = build_embed(
        title=f"{clock} Time until {format_date(date)} UTC",
        description=description,
    )
    await ctx.send(embed=embed)


async def send_tzinfo(ctx: Union[commands.Context, SlashContext], timezone: str):
    date = parse_date(f"12am {timezone}")
    if isinstance(date, datetime):
        embed = build_embed(
            title=f'Timezone offset for "{timezone}"',
            description=f"Name: {date.strftime('%Z')}\nUTC Offset: {date.strftime('%z')}",
        )
        return await ctx.send(embed=embed)
    # unable to parse date
    embed = error_embed(
        f"Sorry {ctx.author.name}, I didn't understand that.",
        "Make sure to include a valid timezone.",
    )
    await ctx.send(embed=embed)
