import random

from discord.ext import commands
from utils.embedder import build_embed


async def flip_coin(ctx: commands.Context):
    images = {
        "Heads": "https://i.imgur.com/jWbI1TR.png",
        "Tails": "https://i.imgur.com/8jYaAht.png",
    }
    choice = random.choice(list(images.keys()))
    await ctx.send(
        embed=build_embed(
            title="🪙 Coin Flip Results", image=images[choice], footer=choice
        )
    )


async def swap_pawns(ctx: commands.Context, *players):
    players = list(players)
    random.shuffle(players)
    embed = build_embed(title="🏁 Pawn Swap Results")
    embed.add_field(name="♔ White", value=players[0])
    embed.add_field(name="♚ Black", value=players[1])
    await ctx.send(embed=embed)
