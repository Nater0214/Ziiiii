# src/bot/cogs/mc.py
# A cog for minecraft server commands


# Imports
from os import getenv

from discord import ApplicationContext, AutocompleteContext, Bot, Option, SlashCommandGroup
from discord.ext.commands import Cog
from discord.utils import basic_autocomplete

from src import craftycontroller


# Definitions
class Minecraft(Cog):
    """Minecraft commands using Crafty Controller"""

    # Command group
    command_group = SlashCommandGroup("mc", "Minecraft server commands", guild_ids=[getenv("HOME_GUILD_ID")])


    # Autocompleters
    @staticmethod
    async def get_servers_autocomplete(ctx: AutocompleteContext) -> list[str]:

        # Defer the interaction
        await ctx.interaction.response.defer()

        # Return the list of servers
        return craftycontroller.api.get_server_names()


    # Commands
    @command_group.command()
    async def start(self, ctx: ApplicationContext, server: Option(str, autocomplete=basic_autocomplete(get_servers_autocomplete), description="The server to start")): # type: ignore
        """Start a minecraft server"""

        # Check if server exists
        if server not in await craftycontroller.api.get_server_names():
            await ctx.response.send_message(f"Server *{server}* does not exist")
            return

        # Respond with start
        await ctx.response.send_message(f"Starting server *{server}*")

        # Get the server id from the server name
        id_ = (await craftycontroller.api.get_name_map())[server]

        # Start the server with the id
        await craftycontroller.api.start_server(id_)


def setup(bot: Bot):
    bot.add_cog(Minecraft(bot))
