import re
import discord
from discord.ext import commands
from discord_components.interaction import Interaction, InteractionType
from discord_slash.context import SlashContext


async def get_channel_ctx(ctx: SlashContext, bot: commands.Bot) -> commands.Context:
    message = await ctx.channel.send("<a:loading:849106660529274930>")
    channel_ctx = await bot.get_context(message)
    await message.delete()
    return channel_ctx


async def accept_challenge(res: Interaction):
    player_id, challenger_id = re.findall(r"\d{10,}", res.message.content)

    if player_id != str(res.user.id):
        await res.respond(
            type=InteractionType.ChannelMessageWithSource,
            content="You are not the recipient of this challenge!",
        )
        return

    await res.respond(
        type=InteractionType.ChannelMessageWithSource,
        content="You have accepted the challenge!",
    )

    await res.message.channel.send(
        f"<@{challenger_id}>, your match against <@{player_id}> has been accepted!"
    )


async def confirm_victory(res: Interaction):
    winner_id, loser_id = re.findall(r"\d{10,}", res.message.content)

    if loser_id != str(res.user.id):
        await res.respond(
            type=InteractionType.ChannelMessageWithSource,
            content="You are not the recipient of this challenge!",
        )
        return

    if res.component.label == "YES":
        await res.respond(
            type=InteractionType.ChannelMessageWithSource,
            content=f"You have confirmed <@{winner_id}> has won!",
        )

        await res.message.channel.send(
            f"<@{loser_id}>, has confirmed <@{winner_id}> has won!"
        )

    elif res.component.label == "NO":
        await res.respond(
            type=InteractionType.ChannelMessageWithSource,
            content=f"You have denied that <@{winner_id}> has won.",
        )

        await res.message.channel.send(
            f"<@{loser_id}>, has denied that <@{winner_id}> has won."
        )


async def get_opponent(user: discord.Member) -> int:
    # TODO: implement
    return 310618854734954497
