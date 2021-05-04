import config
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_choice, create_option
from utils.embedder import build_embed, error_embed

from . import lichess
from .options import Variant, TimeMode, Color


class Lichess(commands.Cog, name="🐴 Lichess"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_subcommand(
        base="play",
        name="live",
        description=(
            "Get a live game URL on Lichess - for standard 10|10, just type /play live"
        ),
        guild_ids=[config.GUILD_ID],
        options=[
            create_option(
                name="minutes",
                description="Minutes on the clock (defaults to 10)",
                option_type=SlashCommandOptionType.INTEGER,
                required=False,
            ),
            create_option(
                name="increment",
                description="Seconds to increment clock each turn (defaults to 10)",
                option_type=SlashCommandOptionType.INTEGER,
                required=False,
            ),
            create_option(
                name="start_color",
                description="Color to go first",
                option_type=SlashCommandOptionType.STRING,
                required=False,
                choices=[
                    create_choice(name="Random", value=Color.RANDOM.value),
                    create_choice(name="White", value=Color.WHITE.value),
                    create_choice(name="Black", value=Color.BLACK.value),
                ],
            ),
            create_option(
                name="variant",
                description="Chess variant",
                option_type=SlashCommandOptionType.INTEGER,
                required=False,
                choices=[
                    create_choice(name="Standard", value=1),
                    create_choice(name="Crazyhouse", value=10),
                    create_choice(name="Chess960", value=2),
                    create_choice(name="King of the Hill", value=4),
                    create_choice(name="Three-check", value=5),
                    create_choice(name="Antichess", value=6),
                    create_choice(name="Atomic", value=7),
                    create_choice(name="Horde", value=8),
                    create_choice(name="Racing Kings", value=9),
                ],
            ),
        ],
    )
    async def play_live_slash(
        self,
        ctx: SlashContext,
        minutes: int = 10,
        increment: int = 10,
        start_color: str = Color.RANDOM.value,
        variant: int = Variant.STANDARD.value,
    ):
        """Slash command: Create a live game on Lichess with custom settings"""
        await ctx.defer()
        if minutes < 0 or increment < 0:
            return await ctx.send(
                embed=error_embed("Minutes and increment must be positive")
            )
        await lichess.send_invite(
            ctx,
            time_mode=TimeMode.REALTIME.value,
            start_color=start_color,
            variant=variant,
            minutes=minutes,
            increment=increment,
        )

    @cog_ext.cog_subcommand(
        base="play",
        name="daily",
        description=(
            "Get a correspondence or unlimited URL on Lichess - for unlimited time, just type /play daily"
        ),
        guild_ids=[config.GUILD_ID],
        options=[
            create_option(
                name="days",
                description="Days on the clock or -1 for Unlimited (defaults to -1)",
                option_type=SlashCommandOptionType.INTEGER,
                required=False,
            ),
            create_option(
                name="start_color",
                description="Color to go first",
                option_type=SlashCommandOptionType.STRING,
                required=False,
                choices=[
                    create_choice(name="Random", value=Color.RANDOM.value),
                    create_choice(name="White", value=Color.WHITE.value),
                    create_choice(name="Black", value=Color.BLACK.value),
                ],
            ),
            create_option(
                name="variant",
                description="Chess variant",
                option_type=SlashCommandOptionType.INTEGER,
                required=False,
                choices=[
                    create_choice(name="Standard", value=1),
                    create_choice(name="Crazyhouse", value=10),
                    create_choice(name="Chess960", value=2),
                    create_choice(name="King of the Hill", value=4),
                    create_choice(name="Three-check", value=5),
                    create_choice(name="Antichess", value=6),
                    create_choice(name="Atomic", value=7),
                    create_choice(name="Horde", value=8),
                    create_choice(name="Racing Kings", value=9),
                ],
            ),
        ],
    )
    async def play_daily_slash(
        self,
        ctx: SlashContext,
        days: int = -1,
        start_color: str = Color.RANDOM.value,
        variant: int = Variant.STANDARD.value,
    ):
        """Slash command: Create a game on Lichess with custom settings"""
        await ctx.defer()
        await lichess.send_invite(
            ctx,
            time_mode=(
                TimeMode.CORRESPONDENCE.value if days > 0 else TimeMode.UNLIMITED.value
            ),
            start_color=start_color,
            variant=variant,
            days=(days if days > 0 else 2),  # days must be positive even if unused
        )

    @cog_ext.cog_subcommand(
        base="game",
        name="status",
        description=("Get the status of a Lichess game"),
        guild_ids=[config.GUILD_ID],
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
        game_id = "".join(ch for ch in game_id if ch.isalpha() or ch.isdigit())[-8:]
        await lichess.send_game_status(ctx, game_id)


def setup(bot: commands.Bot):
    bot.add_cog(Lichess(bot))
