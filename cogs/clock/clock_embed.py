import discord
from datetime import datetime

__clock_emoji = "🕛🕧🕐🕜🕑🕝🕒🕞🕓🕟🕔🕠🕕🕡🕖🕢🕗🕣🕘🕤🕙🕥🕚🕦"


def clock_embed() -> discord.Embed:
    """Generates embed with current time UTC"""
    now = datetime.utcnow()
    clock = __clock_emoji[round(2 * (now.hour % 12 + now.minute / 60)) % len(__clock_emoji)]
    return discord.Embed(
        title=f"{clock} The current time is {now.strftime('%d %B %H:%M UTC')}"
    )