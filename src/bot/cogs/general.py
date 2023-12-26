# src/bot/cogs/general.py
# General commands


# Imports
from os import getenv
from random import choice

from discord import ApplicationContext
from discord.ext import commands


# Definitions
class General(commands.Cog):
    """General commands"""
    
    # Commands
    @commands.slash_command(help="A friendly greeting")
    async def hello(self, ctx: ApplicationContext):
        """Send a friendly greeting"""
        
        await ctx.response.send_message(f"{choice(['Hi', 'Hello', 'Hey', 'Howdy', 'Greetings'])} {ctx.user.display_name}")
    
    
    @commands.slash_command(help="Tells where the bot is (where the command is executed)")
    async def whereareyou(self, ctx: ApplicationContext):
        """Respond where the bot currently is"""
        
        if ctx.guild is not None:
            if ctx.guild.id == int(getenv("HOME_GUILD_ID")):
                await ctx.response.send_message(f"I am at home in the {ctx.channel.name} channel.")
            else:
                await ctx.response.send_message(f"I am in a server named {ctx.guild.name} in the {ctx.channel.name} channel.")
        else:
            await ctx.response.send_message("I am in a DM channel.")