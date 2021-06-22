from discord_components.interaction import Interaction
from cogs.challenge.challenge import (
    accept_challenge,
    confirm_victory,
    get_channel_ctx,
    get_opponent,
)
from utils.embedder import build_embed, error_embed
from discord_components.client import DiscordComponents
import config
import discord
from discord.ext import commands
from discord.ext.commands.cog import Cog
from discord_components import Button, ButtonStyle, InteractionType
from discord_slash import SlashContext, cog_ext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
import re


class Challenge(commands.Cog, name="⚔️ Challenge"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="challenge",
        description=("Challenge an opponent"),
        guild_ids=[config.GUILD_ID],
        options=[
            create_option(
                name="player",
                description="Player to challenge to a match",
                option_type=SlashCommandOptionType.USER,
                required=True,
            ),
        ],
    )
    async def challenge(self, ctx: SlashContext, player: discord.Member):
        """Slash command: challenge a player to a match"""
        if player == ctx.author:
            return await ctx.send(
                embeds=[error_embed("You cannot challenge yourself!")], hidden=True
            )
        await ctx.send(
            "<a:success_a:797816120044158976> Creating challenge!", hidden=True
        )
        channel_ctx = await get_channel_ctx(ctx, self.bot)
        await channel_ctx.send(
            f"{player.mention}, you have been challenged by "
            f"{ctx.author.mention}!\nDo you accept the challenge?",
            components=[Button(style=ButtonStyle.green, label="ACCEPT", emoji="♟️")],
        )

    @cog_ext.cog_slash(
        name="victory",
        description=("Declare that you have won a challenge"),
        guild_ids=[config.GUILD_ID],
        options=[],
    )
    async def victory(self, ctx: SlashContext):
        """Slash command: challenge a player to a match"""
        opponent = await get_opponent(ctx.author)
        await ctx.send("You have declared that you have won!", hidden=True)
        channel_ctx = await get_channel_ctx(ctx, self.bot)
        await channel_ctx.send(
            f"{ctx.author.mention} claims they have won!\n"
            f"<@{opponent}> Do you confirm?",
            components=[
                [
                    Button(style=ButtonStyle.green, label="YES", emoji="👍"),
                    Button(style=ButtonStyle.red, label="NO", emoji="👎"),
                ]
            ],
        )

    @Cog.listener()
    async def on_button_click(self, res: Interaction):
        if res.component.label == "ACCEPT":
            return await accept_challenge(res)

        await confirm_victory(res)


def setup(bot: commands.Bot):
    DiscordComponents(bot)
    bot.add_cog(Challenge(bot))
