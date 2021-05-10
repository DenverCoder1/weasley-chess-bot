import config
import discord
from discord.ext import commands

from .scoreboard import check_and_update_channel


class Scoreboard(commands.Cog, name="🧮 Scoreboard"):
    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__channel: discord.TextChannel

    @commands.Cog.listener()
    async def on_ready(self):
        """When bot is ready"""
        # get scoreboard channel object
        self.__channel = self.__bot.get_channel(config.SCOREBOARD_CHANNEL_ID)
        # check that channel exists
        if not isinstance(self.__channel, discord.TextChannel):
            print("Couldn't find that channel.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """When a message is received in the scoreboard channel"""
        await check_and_update_channel(message, self.__bot, self.__channel)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """When a message is deleted in the scoreboard channel"""
        await check_and_update_channel(message, self.__bot, self.__channel)

    @commands.Cog.listener()
    async def on_message_edit(self, message: discord.Message):
        """When a message is edited in the scoreboard channel"""
        await check_and_update_channel(message, self.__bot, self.__channel)


def setup(bot):
    bot.add_cog(Scoreboard(bot))
