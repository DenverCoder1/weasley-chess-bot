import re
from typing import Dict, Optional

import discord
from discord.ext import commands
from utils.logging import log_to_channel

from .validation_error import ValidationError


async def __extract_points_from_line(line: str) -> tuple[int]:
    """Returns a tuple corresponding to points for Hogwarts, Beauxbatons, and Durmstrang"""
    match = re.search(
        r"\| (\w+) p\w*ts? .*\b(each|[Hh]og\w*|[Bb]ea\w*|[Dd]ur\w*)\b", line
    )
    if not match:
        if not re.match(r"^[A-Z][a-z]+:(?: \d+)?", line) and line.strip() != "":
            raise ValidationError(f"ERROR: points not found: '{line}'")
        return 0, 0, 0
    points = int(match[1].replace("one", "1").replace("two", "2").replace("three", "3"))
    if match[2] == "each":
        hog = int(re.search(r"^[^|]+\([Hh]og\w*\)[^|]+\|", line) is not None)
        beaux = int(re.search(r"^[^|]+\([Bb]ea\w*\)[^|]+\|", line) is not None)
        durm = int(re.search(r"^[^|]+\([Dd]ur\w*\)[^|]+\|", line) is not None)
        if hog + beaux + durm != 2:
            raise ValidationError(f"ERROR: more than 2 teams found: '{line}'")
        return hog * points, beaux * points, durm * points
    if re.match(r"[Hh]og\w*", match[2]):
        return points, 0, 0
    if re.match(r"[Bb]ea\w*", match[2]):
        return 0, points, 0
    if re.match(r"[Dd]ur\w*", match[2]):
        return 0, 0, points
    raise ValidationError(f"ERROR: team not found: '{line}'")


async def __calculate_totals(
    bot: commands.Bot, channel: discord.TextChannel
) -> Dict[str, int]:
    """Count the scores of messages posted to scoreboard channel"""
    totals = {
        "Hog": 0,
        "Beaux": 0,
        "Durm": 0,
    }
    first = True
    async for message in channel.history(limit=200):
        lines = message.content.split("\n")
        for line in lines:
            try:
                hog, beaux, durm = await __extract_points_from_line(line)
                totals["Hog"] += hog
                totals["Beaux"] += beaux
                totals["Durm"] += durm
                if any(r.emoji == "🤔" for r in message.reactions):
                    try:
                        await message.remove_reaction("🤔", bot.user)
                    except Exception:
                        pass
            except ValidationError as err:
                await message.add_reaction("🤔")
                if first:
                    await log_to_channel(bot, err.message)
        first = False
    return totals


def __to_sub(text: str) -> str:
    return str(text).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))


async def __new_channel_name(bot: commands.Bot, channel: discord.TextChannel) -> str:
    """Count the scores of messages posted to scoreboard channel"""
    totals = await __calculate_totals(bot, channel)
    return f"score︱ʜ{__to_sub(totals['Hog'])}・ʙ{__to_sub(totals['Beaux'])}・ᴅ{__to_sub(totals['Durm'])}"


async def check_and_update_channel(
    bot: commands.Bot,
    channel: discord.TextChannel,
    message: Optional[discord.Message] = None,
):
    if message and message.channel.id != channel.id:
        return
    # update channel name if it has changed
    channel_name = await __new_channel_name(bot, channel)
    if channel.name != channel_name:
        await channel.edit(name=channel_name)
