from typing import Dict
from discord_slash.context import SlashContext
from utils.embedder import build_embed

import lichess.api as lc
import play_lichess

__lichess_logo = "https://i.imgur.com/AA0Y84u.png"


async def send_invite(ctx: SlashContext, **kwargs):
    footer = "The first two people to come to this URL will play"
    try:
        match = play_lichess.create(**kwargs)
        title, link = match.title, match.link
    except play_lichess.exceptions.HttpError as error:
        title, link = (
            "lichess.org • Free Online Chess",
            "https://lichess.org/setup/friend",
        )
        footer = error.args[0]
    embed = build_embed(
        title=title,
        description=link,
        footer=footer,
        thumbnail=__lichess_logo,
    )
    await ctx.send(embed=embed)


def __get_winner(game: Dict):
    winner = game.get("winner")
    if winner:
        return __user_str(game["players"][winner], False)
    return None


def __user_str(player: Dict, include_rating: bool = True):
    if not player.get("user"):
        return "Anonymous"
    user_str = player["user"]["name"]
    if player.get("rating") and include_rating:
        user_str += f" ({player['rating']})"
    return user_str


def __game_status(game: Dict):
    if game.get("status") == "draw":
        return "Game ended in a draw"
    if __get_winner(game):
        return __get_winner(game) + " won the game"
    return "Game is in progress"


async def send_game_status(ctx: SlashContext, game_id: str):
    try:
        game = lc.game(game_id)
        player1 = game["players"]["white"]
        player2 = game["players"]["black"]
        status = __game_status(game)
        game_info = f"**{game['variant'].capitalize()} • {game['speed'].capitalize()}**"
        players = __user_str(player1) + " vs. " + __user_str(player2)
        embed = build_embed(
            title=status,
            url=f"https://lichess.org/{game_id}",
            description=game_info + "\n" + players,
            thumbnail=__lichess_logo,
        )
        await ctx.send(embed=embed)
    except lc.ApiHttpError:
        embed = build_embed("Game has not yet started or doesn't exist")
        await ctx.send(embed=embed)
