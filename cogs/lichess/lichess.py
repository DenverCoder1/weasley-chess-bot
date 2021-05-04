from typing import Dict, Tuple

import requests
from discord_slash.context import SlashContext
from utils.embedder import build_embed

import lichess.api as lc

__lichess_logo = "https://i.imgur.com/AA0Y84u.png"


def __get_invite(
    time_mode: int,
    start_color: str,
    variant: int,
    minutes: int = 10,
    increment: int = 10,
    days: int = 2,
) -> Tuple[str]:
    """Get an invite title and url for a new game on Lichess"""
    url = "https://lichess.org/setup/friend"
    data = {
        "variant": variant,
        "fen": "",
        "timeMode": time_mode,
        "time": minutes,  # only for real time
        "increment": increment,  # only for real time
        "days": days,  # only for correspondence
        "color": start_color,
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.post(
        url,
        data=data,
        headers=headers,
    )
    text = response.text
    title = text[text.find("<title>") + 7 : text.find("</title>")]
    # get redirect url where game will start
    redirect_url = response.url
    # check that the url was redirected to a game url
    if redirect_url == url:
        raise ConnectionError(f"Error {response.status_code}: {response.reason}")
    return title, redirect_url


def __get_game_by_id(game_id: str) -> Dict[str, str]:
    return lc.game(game_id[-8:])


async def send_invite(ctx: SlashContext, **kwargs):
    footer = "The first two people to come to this URL will play"
    try:
        title, url = __get_invite(**kwargs)
    except ConnectionError as error:
        title, url = (
            "lichess.org • Free Online Chess",
            "https://lichess.org/setup/friend",
        )
        footer = error.args[0]
    embed = build_embed(
        title=title,
        description=url,
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
        game = __get_game_by_id(game_id)
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
