from datetime import datetime

from discord.ext import commands
from utils.dates import format_date, parse_date, get_clock_emoji
from utils.embedder import build_embed


async def to_utc(ctx: commands.Context, date_str: str):
    utc_date = parse_date(date_str, to_tz="UTC")
    await embed_time(ctx, utc_date, date_str)


async def embed_time(
    ctx: commands.Context, date: datetime, input: str, timezone: str = "UTC"
):
    clock = get_clock_emoji(date)
    embed = build_embed(
        title=f"{clock} {format_date(date)} {timezone}",
        description=f'Converted to {timezone} from "{input}"',
    )
    await ctx.send(embed=embed)
