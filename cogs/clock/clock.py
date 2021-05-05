from datetime import datetime

import discord
from discord.ext import commands
from utils.dates import format_date, get_clock_emoji
from utils.embedder import build_embed


def clock_embed() -> discord.Embed:
    """Generates embed with current time UTC"""
    now = datetime.utcnow()
    clock = get_clock_emoji(now)
    return build_embed(title=f"{clock} The current time is {format_date(now)} UTC")


async def get_or_create_message(
    bot: commands.Bot, channel: discord.TextChannel
) -> discord.Message:
    # get message if there's one in the past 20 messages
    message = await channel.history(limit=20).get(author__id=bot.user.id)
    # create new message if there's none
    if not message:
        message = await channel.send(embed=clock_embed())
    return message


async def update_clock_channel_name(channel: discord.TextChannel):
    now = datetime.utcnow()
    clock = get_clock_emoji(now)
    await channel.edit(
        name=f"clock︱{clock} {now.strftime('%H')}꞉{now.strftime('%M')} 𝖴𝖳𝖢"
    )
