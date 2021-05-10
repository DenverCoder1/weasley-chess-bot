from discord.ext import commands
import config
from .embedder import build_embed


async def log_to_channel(bot: commands.Bot, text: str):
    channel = bot.get_channel(config.LOGGING_CHANNEL_ID)
    await channel.send(embed=build_embed(text))
