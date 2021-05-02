import discord
from discord.ext.tasks import loop
from discord.ext import commands
from .clock_embed import clock_embed

import config

CHECK_INTERVAL_SECONDS = 60 # every minute

class ClockCog(commands.Cog, name="Clock"):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		"""When discord is connected"""
		# Start clock
		self.clock.start()
		print("Starting clock...")

	@commands.Cog.listener()
	async def on_message_delete(self, message: discord.Message):
		"""Recreate message on deletion"""
		# check id is the clock's message
		if message.id == self.__message.id:
			# get message if there's one in the past 2 messages
			self.__message = await self.__channel.history(limit=2).get(author__id=self.bot.user.id)
			# create new message if there's none
			if not self.__message:
				self.__message = await self.__channel.send(embed=clock_embed())

	@loop(seconds=CHECK_INTERVAL_SECONDS)
	async def clock(self):
		"""loop to update clock"""
		# update the clock
		await self.__message.edit(embed=clock_embed())

	@clock.before_loop
	async def clock_init(self):
		"""print startup info before reddit feed loop begins"""
		# get clock channel object
		self.__channel = self.bot.get_channel(config.CLOCK_CHANNEL_ID)
		# if channel exists, get the last message from the bot
		if isinstance(self.__channel, discord.TextChannel):
			self.__message = await self.__channel.history().get(author__id=self.bot.user.id)
		# if no messages found, send a new one
		if not self.__message:
			self.__message = await self.__channel.send(embed=clock_embed())

def setup(bot):
	bot.add_cog(ClockCog(bot))
