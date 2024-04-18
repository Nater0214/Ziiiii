# src/bot/cogs/__init__.py
# Load the cogs


# Imports
from .general import General
from .mc import Minecraft
from .music import Music
from .shadowbox import Shadowbox


# Definitions
def setup(bot):
    bot.add_cog(General(bot))
    bot.add_cog(Music(bot))
    # bot.add_cog(Minecraft(bot))
    bot.add_cog(Shadowbox(bot))
