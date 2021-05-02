import discord
from datetime import datetime

def clock_embed() -> discord.Embed:
    """Generates embed with current time UTC"""
    return discord.Embed(
        title="🕝 The current time is " + datetime.utcnow().strftime("%d %B %H:%M UTC")
    )