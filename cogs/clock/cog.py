import config
import discord
from discord.errors import HTTPException
from discord.ext import commands
from discord.ext.tasks import loop
from datetime import datetime

from .clock import (
    clock_embed,
    get_or_create_message,
    new_channel_name,
    get_embed_title,
)


class Clock(commands.Cog, name="🕒 Clock"):
    def __init__(self, bot: commands.Bot):
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """When discord is connected"""
        # Start clock
        self.clock.start()
        print("Starting clock...")

    @loop(seconds=1)
    async def clock(self):
        """Loop to check and update clock"""
        # update the clock message
        try:
            embed = clock_embed()
            # update only if the time is different
            if embed.title != get_embed_title(self.__message):
                # edit the message
                await self.__message.edit(embed=embed)
        except HTTPException:
            # if message doesn't exist, create a new one
            self.__message = await get_or_create_message(self.__bot, self.__channel)
        # update channel name if it has changed
        channel_name = new_channel_name()
        if self.__channel.name != channel_name:
            await self.__channel.edit(name=channel_name)

    @clock.before_loop
    async def clock_init(self) -> None:
        """print startup info before reddit feed loop begins"""
        # get clock channel object
        self.__channel = self.__bot.get_channel(config.CLOCK_CHANNEL_ID)
        # check that channel exists
        if not isinstance(self.__channel, discord.TextChannel):
            print("Couldn't find that channel.")
            return self.clock.cancel()
        # if channel exists, get the last message from the bot or create one
        self.__message = await get_or_create_message(self.__bot, self.__channel)


def setup(bot):
    bot.add_cog(Clock(bot))
