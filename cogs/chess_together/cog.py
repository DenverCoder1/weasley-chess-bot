from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_choice, create_option
from discordTogether import DiscordTogether
import config


class DiscordTogetherCog(commands.Cog, name="Discord Together"):
    def __init__(self, bot: commands.Bot):
        self.__dt = DiscordTogether(bot)

    async def _start_activity(self, ctx: SlashContext, name: str):
        if ctx.author.voice is None:
            return await ctx.send("You must be in a voice channel to start an activity.")
        # Here we consider that the user is already in a VC accessible to the bot.
        link = await self.__dt.create_link(ctx.author.voice.channel.id, name)
        await ctx.send(f"Click the blue link!\n{link}")

    @cog_ext.cog_subcommand(
        base="vc",
        name="chess",
        description=("Start a game of Chess in the Park"),
        guild_ids=[config.GUILD_ID],
    )
    async def vc_chess_slash(self, ctx: SlashContext):
        await self._start_activity(ctx, "chess")

    @cog_ext.cog_subcommand(
        base="vc",
        name="activity",
        description=("Start a voice channel activity"),
        guild_ids=[config.GUILD_ID],
        options=[
            create_option(
                name="activity",
                description="Activity to play",
                option_type=SlashCommandOptionType.STRING,
                required=False,
                choices=[
                    create_choice(name="YouTube Together", value="youtube"),
                    create_choice(name="Poker Night", value="poker"),
                    create_choice(name="Chess in the Park", value="chess"),
                    create_choice(name="Betrayal.io", value="betrayal"),
                    create_choice(name="Fishington.io", value="fishing"),
                ],
            ),
        ]
    )
    async def vc_activity_slash(self, ctx: SlashContext, activity: str = "chess"):
        await self._start_activity(ctx, activity)


def setup(client):
    client.add_cog(DiscordTogetherCog(client))
