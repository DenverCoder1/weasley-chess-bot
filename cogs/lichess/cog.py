import config
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_choice, create_option
from utils.embedder import error_embed

from . import lichess
from play_lichess.constants import Variant, TimeMode, Color


class Lichess(commands.Cog, name="🐴 Lichess"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_subcommand(
        base="play",
        name="live",
        description=(
            "Get a live game URL on Lichess - for blitz 5+0, just type /play live"
        ),
        guild_ids=config.GUILD_IDS,
        options=[
            create_option(
                name="minutes",
                description="Minutes on the clock (defaults to 5)",
                option_type=SlashCommandOptionType.INTEGER,
                required=False,
            ),
            create_option(
                name="increment",
                description="Seconds to increment clock each turn (defaults to 0)",
                option_type=SlashCommandOptionType.INTEGER,
                required=False,
            ),
            create_option(
                name="variant",
                description="Chess variant (defaults to Standard)",
                option_type=SlashCommandOptionType.STRING,
                required=False,
                choices=[
                    create_choice(name=option.description,
                                  value=option.description)
                    for option in list(Variant)
                    if option != Variant.FROM_POSITION
                ],
            ),
            create_option(
                name="color",
                description="Color the first player to join will play (defaults to Random)",
                option_type=SlashCommandOptionType.STRING,
                required=False,
                choices=[
                    create_choice(name=option.description,
                                  value=option.description)
                    for option in list(Color)
                ],
            ),
        ],
    )
    async def play_live_slash(
        self,
        ctx: SlashContext,
        minutes: int = 5,
        increment: int = 0,
        color: str = Color.RANDOM.description,
        variant: int = Variant.STANDARD.description,
    ):
        """Slash command: Create a live game on Lichess with custom settings"""
        await ctx.defer()
        if minutes < 0 or increment < 0:
            return await ctx.send(
                embed=error_embed("Minutes and increment must be non-negative")
            )
        await lichess.send_invite(
            ctx,
            time_mode=TimeMode.REALTIME,
            color=Color.find(color),
            variant=Variant.find(variant),
            minutes=minutes,
            increment=increment,
        )

    @cog_ext.cog_subcommand(
        base="play",
        name="daily",
        description=(
            "Get a correspondence or unlimited URL on Lichess - for unlimited time, just type /play daily"
        ),
        guild_ids=config.GUILD_IDS,
        options=[
            create_option(
                name="days",
                description="Days on the clock or -1 for Unlimited (defaults to -1)",
                option_type=SlashCommandOptionType.INTEGER,
                required=False,
            ),
            create_option(
                name="variant",
                description="Chess variant (defaults to Standard)",
                option_type=SlashCommandOptionType.STRING,
                required=False,
                choices=[
                    create_choice(name=option.description,
                                  value=option.description)
                    for option in list(Variant)
                    if option != Variant.FROM_POSITION
                ],
            ),
            create_option(
                name="color",
                description="Color the first player to join will play (defaults to Random)",
                option_type=SlashCommandOptionType.STRING,
                required=False,
                choices=[
                    create_choice(name=option.description,
                                  value=option.description)
                    for option in list(Color)
                ],
            ),
        ],
    )
    async def play_daily_slash(
        self,
        ctx: SlashContext,
        days: int = -1,
        color: str = Color.RANDOM.description,
        variant: int = Variant.STANDARD.description,
    ):
        """Slash command: Create a game on Lichess with custom settings"""
        await ctx.defer()
        await lichess.send_invite(
            ctx,
            time_mode=TimeMode.CORRESPONDENCE if days > 0 else TimeMode.UNLIMITED,
            color=Color.find(color),
            variant=Variant.find(variant),
            # days must be positive even if unused
            days=(days if days > 0 else 2),
        )

    @cog_ext.cog_subcommand(
        base="game",
        name="status",
        description=("Get the status of a Lichess game"),
        guild_ids=config.GUILD_IDS,
        options=[
            create_option(
                name="game_id",
                description="Lichess URL or 8-character game ID",
                option_type=SlashCommandOptionType.STRING,
                required=True,
            )
        ],
    )
    async def game_status_slash(self, ctx: SlashContext, game_id: str):
        """Slash command: Create a game on Lichess with custom settings"""
        await ctx.defer()
        # strip non alphanumeric characters
        game_id = "".join(ch for ch in game_id if ch.isalpha()
                          or ch.isdigit())[-8:]
        await lichess.send_game_status(ctx, game_id)


def setup(bot: commands.Bot):
    bot.add_cog(Lichess(bot))
