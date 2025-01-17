# import os
# from datetime import date
# from pathlib import Path

# from discord import Interaction, TextChannel, app_commands
from discord.ext import commands, tasks
from discord.ext.commands import Bot

from utils.channel_data import get_channel_from_name
from utils.config import get_config
from utils.env import get_twitch_client, get_twitch_secret, get_twitch_user
from utils.twitch_online import is_twitch_online

# from dotenv import load_dotenv


class TwitchListen(commands.Cog):
    """
    Twitch listen.

    Cog for Twitch listen.
    """

    bot: Bot
    is_live: bool
    last_seen_live: bool

    def __init__(self, bot: Bot):
        self.bot = bot
        self.is_live = False
        self.last_seen_live = False

    def cog_unload(self) -> None:
        """
        Unload method.

        Called when Cog unloads.
        """
        try:
            self.twitch.cancel()
        except Exception as e:
            print(f"Stopping the twitch listener failed - error: {e}")

    def cog_load(self) -> None:
        """
        Load method.

        Called when Cog loads.
        """
        try:
            self.twitch.start()
        except Exception as e:
            print(f"Starting the twitch listener failed - error: {e}")

    @tasks.loop(seconds=5.0)
    async def twitch(self) -> None:
        """
        Announces to channels in config when twitch account becomes online.

        Parameters (None)

        Interfaces with
        ----------
            List of discord channels pulled from config

        Returns
        ----------
            None, but sends message in each discord channel when live.
        """
        self.is_live = is_twitch_online(get_twitch_client(), get_twitch_secret(), get_twitch_user())

        # send message only if currently live and not previously
        if self.is_live:
            if not self.last_seen_live:
                twitch_channels = get_config("twitch_announcement_channels")
                for channel_name in twitch_channels:
                    channel = get_channel_from_name(self.bot, channel_name)
                    if channel is None:
                        print("Fetching channel from ID failed. Perhaps wrong server.")
                    else:
                        await channel.send("Splatoon Stronghold is now live! https://twitch.tv/SplatoonStronghold")

            self.last_seen_live = True
        else:
            self.last_seen_live = False
