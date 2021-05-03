import discord
from datetime import datetime

from discord.ext import commands

__clock_emoji = "🕛🕧🕐🕜🕑🕝🕒🕞🕓🕟🕔🕠🕕🕡🕖🕢🕗🕣🕘🕤🕙🕥🕚🕦"


def clock_embed() -> discord.Embed:
    """Generates embed with current time UTC"""
    now = datetime.utcnow()
    clock = __clock_emoji[round(2 * (now.hour % 12 + now.minute / 60)) % len(__clock_emoji)]
    return discord.Embed(
        title=f"{clock} The current time is {now.strftime('%d %B %H:%M UTC')}",
        colour=discord.Colour.blurple()
    )

async def get_or_create_embed(bot: commands.Bot, channel: discord.TextChannel) -> discord.Embed:
    # get message if there's one in the past 20 messages
    message = await channel.history(limit=20).get(
        author__id=bot.user.id
    )
    # create new message if there's none
    if not message:
        message = await channel.send(embed=clock_embed())
    return message