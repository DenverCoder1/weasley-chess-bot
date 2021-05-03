from typing import Union
from .random import flip_coin, swap_pawns
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
import config


class Random(commands.Cog, name="🎲 Random"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="coinflip",
        description=("Flip a coin."),
        guild_ids=[config.GUILD_ID],
        options=[],
    )
    @commands.command(aliases=["flip", "coin", "flipcoin", "flip_coin"])
    async def coinflip_slash(self, ctx: SlashContext):
        """Slash command: replies "Heads" or "Tails" at random."""
        await flip_coin(ctx)

    @commands.command(aliases=["flip", "coin", "flipcoin", "flip_coin"])
    async def coinflip(self, ctx: commands.Context):
        """Replies "Heads" or "Tails" at random.
        ```
        -coinflip
        ```
        """
        await flip_coin(ctx)

    @cog_ext.cog_slash(
        name="pawnswap",
        description=("Swap pawns between two players."),
        guild_ids=[config.GUILD_ID],
        options=[
            create_option(
                name="player_1",
                description="Name or mention of Player 1",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            ),
            create_option(
                name="player_2",
                description="Name or mention of Player 2",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            ),
        ],
    )
    async def pawnswap_slash(self, ctx: SlashContext, player_1: str, player_2: str):
        """Slash command: Takes names of both players and assigns "White" to one and "Black" to the other."""
        await swap_pawns(ctx, player_1, player_2)

    @commands.command(aliases=["pawn", "swap", "swappawns", "pawn_swap", "swap_pawns"])
    async def pawnswap(self, ctx: commands.Context, player_1: str, player_2: str):
        """Takes names of both players and assigns "White" to one and "Black" to the other.
        ```
        -pawnswap Eyl Panda
        ```
        """
        await swap_pawns(ctx, player_1, player_2)


def setup(bot: commands.Bot):
    bot.add_cog(Random(bot))
