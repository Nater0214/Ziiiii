# src/bot/modules/purge.py
# A cog for message purging commands


# Imports
from discord import ApplicationContext, Bot, NotFound, Option, Permissions, SlashCommandGroup
from discord.ext.commands import Cog


# Definitions
class Purge(Cog):
    """Message purging commands"""

    # Permissions
    permissions = Permissions()
    permissions.manage_messages = True


    # Command group
    command_group = SlashCommandGroup("purge", "Commands for purging messages and channels", guild_only=True, default_member_permissions=permissions)


    # Commands
    @command_group.command()
    async def all(self, ctx: ApplicationContext):
        """Purge all messages in a channel"""

        # Send status message
        await ctx.response.send_message("Purging all messages in this channel...")

        # Loop through all messages and delete
        async for message in ctx.channel.history():
            await message.delete()


    @command_group.command()
    async def after(self, ctx: ApplicationContext, message_id: Option(str, required=True, description="The id of the first message to purge")): # type: ignore
        """Purge all messages after a specific message"""

        # Check if message exists in this channel
        try:
            first_message = await ctx.channel.fetch_message(int(message_id))
        except ValueError:
            await ctx.response.send_message("The message provided is not a valid message id")
            return
        except NotFound:
            await ctx.response.send_message("The message provided does not exist in this channel")
            return

        # Send status message
        await ctx.response.send_message(f"Purging all messages after {message_id}...")

        # Loop through messages and delete
        async for message in ctx.channel.history():
            await message.delete()

            if message == first_message:
                break


def setup(bot: Bot):
    bot.add_cog(Purge(bot))
