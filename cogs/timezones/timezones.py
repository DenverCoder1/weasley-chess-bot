from datetime import datetime

from discord.ext import commands
from utils.dates import format_date, parse_date, get_clock_emoji
from utils.embedder import build_embed, error_embed


async def to_utc(ctx: commands.Context, date_input: str):
    new_date = parse_date(date_input, to_tz="UTC")
    if isinstance(new_date, datetime) and parse_date(date_input).tzinfo:
        return await embed_time(ctx, new_date, date_input)
    # unable to parse date
    embed = error_embed(
        f"Sorry {ctx.author.name}, I didn't understand that.",
        "Make sure to include a date and timezone. Use `w!help toUTC` for more info.",
    )
    await ctx.send(embed=embed)


async def from_utc(ctx: commands.Context, date_str: str, to_tz: str):
    new_date = parse_date(date_str, from_tz="UTC", to_tz=to_tz)
    if isinstance(new_date, datetime):
        date_input = date_str if "UTC" in date_str else f"{date_str} (UTC)"
        return await embed_time(ctx, new_date, date_input, to_tz)
    # unable to parse date
    embed = error_embed(
        f"Sorry {ctx.author.name}, I didn't understand that.",
        "Make sure to include a date and timezone. Use `w!help fromUTC` for more info.",
    )
    await ctx.send(embed=embed)


async def embed_time(
    ctx: commands.Context, date_output: datetime, date_input: str, timezone: str = "UTC"
):
    clock = get_clock_emoji(date_output)
    embed = build_embed(
        title=f"{clock} {format_date(date_output)} {timezone}",
        description=(f'Converted to {timezone} from "{date_input}"'),
    )
    await ctx.send(embed=embed)
