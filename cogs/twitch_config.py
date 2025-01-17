# import json
# import os
# from pathlib import Path
from typing import List, Union

from discord import Interaction, app_commands

# from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Bot

from utils import env
from utils.config import add_channel, get_config, remove_channel


class TwitchConfig(commands.Cog):
    """
    Twitch config.

    Cog for Twitch config.
    """

    bot: Bot
    twitch_announcement_channels: Union[str, List[str]]

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        print("Twitch config added!")
        self.twitch_announcement_channels = get_config("twitch_announcement_channels")

    @app_commands.command(
        name="config-twitch-publisher", description="Sets the channels to announce twitch livestreams"
    )
    @app_commands.checks.has_any_role("Staff", "Admin")
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    async def config_twitch(self, interaction: Interaction, add: str = None, remove: str = None) -> None:
        """
        Configures discord channels that announce a twitch livestream.

        Parameters
        ----------
        self : Bot
            Bot in discord guild
        interaction : Interaction
            Represents the discord interaction.
        add : String
            A discord channel's name to be added to the configured channels.
        remove : String
            A discord channel's name to be removed from the configured channels.

        Returns
        -------
        (None)
            Sends a discord message on success/failure.
        """
        response = interaction.response
        if add:
            if add in [channel.name for channel in interaction.guild.channels]:
                self.twitch_announcement_channels = add_channel("twitch_announcement_channels", add)
                await response.send_message(
                    content=f'"{add}" has been added to the list of channels to announce twitch livestreams!'
                )
            else:
                await response.send_message(
                    content=f'"{add}" was not added from the list of channels to announce twitch livestreams. '
                    f"Please check that it is spelled correctly and case sensitive"
                )
        if remove:
            if remove in self.twitch_announcement_channels:
                try:
                    self.twitch_announcement_channels = remove_channel("twitch_announcement_channels", remove)
                    await response.send_message(
                        content=f'"{remove}" has been removed from the list of channels to announce twitch livestreams!'
                    )
                except Exception as e:
                    print(e)
                    await response.send_message(
                        content=f'"{remove}" was not removed from the list of channels to announce twitch livestreams. '
                        f"Please check that it is spelled correctly and case sensitive"
                    )
            else:
                await response.send_message(
                    content=f'"{remove}" was not in the list of channels to announce twitch livestreams.'
                )
