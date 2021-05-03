import discord
from discord.errors import HTTPException
from discord.ext.tasks import loop
from discord.ext import commands
from .clock_embed import clock_embed, get_or_create_embed

import config

CHECK_INTERVAL_SECONDS = 60  # every 60 seconds


class ClockCog(commands.Cog, name="Clock"):
    def __init__(self, bot: commands.Bot):
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """When discord is connected"""
        # Start clock
        self.clock.start()
        print("Starting clock...")

    @loop(seconds=CHECK_INTERVAL_SECONDS)
    async def clock(self):
        """loop to update clock"""
        # update the clock
        try:
            await self.__message.edit(embed=clock_embed())
        except HTTPException:
            self.__message = await get_or_create_embed(self.__bot, self.__channel)

    @clock.before_loop
    async def clock_init(self):
        """print startup info before reddit feed loop begins"""
        # get clock channel object
        self.__channel = self.__bot.get_channel(config.CLOCK_CHANNEL_ID)
        # if channel exists, get the last message from the bot
        if isinstance(self.__channel, discord.TextChannel):
            # find the last message from the bot in the channel or create a new one
            self.__message = await get_or_create_embed(self.__bot, self.__channel)
            return
        # error
        print("Couldn't find that channel.")


def setup(bot):
    bot.add_cog(ClockCog(bot))
