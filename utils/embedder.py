import discord
from typing import Optional, Union
from discord.embeds import EmptyEmbed, _EmptyEmbed

GINGER_COLOUR = discord.Color(int("B06500", 16))


def __trim(text: str, limit: int) -> str:
    """limit text to a certain number of characters"""
    return text[: limit - 3].strip() + "..." if len(text) > limit else text


def build_embed(
    title: str,
    description: Optional[str] = None,
    footer: Optional[str] = None,
    image: Optional[str] = None,
    url: Union[str, _EmptyEmbed] = EmptyEmbed,
    colour: discord.Colour = GINGER_COLOUR,
) -> discord.Embed:
    """Embed a message and an optional description, footer, and url"""
    # create the embed
    embed = discord.Embed(title=__trim(title, 256), url=url, colour=colour)
    if description:
        embed.description = __trim(description, 2048)
    if footer:
        embed.set_footer(text=__trim(footer, 2048))
    if image:
        embed.set_image(url=image)
    return embed
