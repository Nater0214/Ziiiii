# src/bot/cogs/mc.py
# A cog for minecraft server commands


# Imports
import subprocess
from os import getenv

from discord import ApplicationContext, Option, SlashCommandGroup
from discord.ext.commands import Cog


# Definitions
class Minecraft(Cog):
    """Minecraft commands"""
    
    # Command group
    command_group = SlashCommandGroup("mc", "Minecraft commands", guild_ids=[getenv("HOME_GUILD_ID")])
    
    
    # Commands
    @command_group.command(guild_only=True)
    async def start(self, ctx: ApplicationContext, server: Option(str, description="The server to start", choices=["blox-smp"])):
        """Starts a minecraft server"""
        
        # Send status message
        await ctx.response.send_message(f"Starting minecraft server {server}...")
        
        # Start the server
        if server == "blox-smp":
            subprocess.Popen(["/var/mc-servers/blox_smp_1/run.sh", "y"])
    
    
    @command_group.command(guild_only=True)
    async def list(self, ctx: ApplicationContext):
        """Lists all minecraft servers"""
        
        await ctx.response.send_message("All Minecraft Servers:\n `blox-smp`: The Blox SMP\nThats it lol")