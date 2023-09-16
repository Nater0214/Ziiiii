# src/bot/__init__.py
# Bot stuff


# Imports
from os import environ

from discord import Activity, ActivityType, Intents, Member, VoiceState
from discord.ext import commands


# Definitions
def run() -> None:
    """Run the bot"""
    
    # Set bot intents
    intents = Intents.default()
    intents.members = True
    intents.message_content = True
    
    # Create bot
    bot = commands.Bot(intents=intents, help_command=None)
    bot.activity = Activity(type=ActivityType.watching, name="Backflipblox")
    
    # Add voice event
    @bot.event
    async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState) -> None:
        if member.id != bot.user.id:
            # Leave voice channel if no one is in it
            if after.channel is None:
                if before.channel.members is None:
                    await member.guild.voice_client.disconnect()
    
    # Add cogs
    bot.load_extension("src.bot.cogs")
    
    # Run the bot
    print("Starting the bot")
    bot.run(environ.get("BOT_TOKEN"))