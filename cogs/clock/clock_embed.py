from datetime import datetime

import discord
from discord.ext import commands
from utils.dates import get_clock_emoji, format_date
from utils.embedder import build_embed


def clock_embed() -> discord.Embed:
    """Generates embed with current time UTC"""
    now = datetime.utcnow()
    clock = get_clock_emoji(now)
    return build_embed(title=f"{clock} The current time is {format_date(now)} UTC")


async def get_or_create_embed(
    bot: commands.Bot, channel: discord.TextChannel
) -> discord.Embed:
    # get message if there's one in the past 20 messages
    message = await channel.history(limit=20).get(author__id=bot.user.id)
    # create new message if there's none
    if not message:
        message = await channel.send(embed=clock_embed())
    return message
