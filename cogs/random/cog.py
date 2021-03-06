import config
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

from .random import flip_coin, swap_pawns


class Random(commands.Cog, name="🎲 Random"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_subcommand(
        base="coin",
        name="flip",
        description=("Flip a coin."),
        guild_ids=config.GUILD_IDS,
        options=[],
    )
    async def coin_flip_slash(self, ctx: SlashContext):
        """Slash command: replies with "Heads" or "Tails" at random."""
        await flip_coin(ctx)

    @commands.command(
        aliases=["flip", "coin", "coinflip",
                 "flipcoin", "flip_coin", "cf", "fc"]
    )
    async def coin_flip(self, ctx: commands.Context):
        """Replies with "Heads" or "Tails" at random.
        ```
        w!coinflip
        ```
        """
        await flip_coin(ctx)

    @cog_ext.cog_subcommand(
        base="pawn",
        name="swap",
        description=("Swap pawns between two players."),
        guild_ids=config.GUILD_IDS,
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
    async def pawn_swap_slash(self, ctx: SlashContext, player_1: str, player_2: str):
        """Slash command: Takes names of both players and assigns "White" to one and "Black" to the other."""
        await swap_pawns(ctx, player_1, player_2)

    @commands.command(
        aliases=["pawn", "swap", "swappawns",
                 "pawnswap", "swap_pawns", "ps", "sp"]
    )
    async def pawn_swap(self, ctx: commands.Context, player_1: str, player_2: str):
        """Takes names of both players and assigns "White" to one and "Black" to the other.
        ```
        w!pawnswap Eyl Panda
        ```
        """
        await swap_pawns(ctx, player_1, player_2)


def setup(bot: commands.Bot):
    bot.add_cog(Random(bot))
