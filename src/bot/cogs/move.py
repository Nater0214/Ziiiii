# src/bot/cogs/move.py
# A cog for vc moving related commands


# Imports
from discord import ApplicationContext, Bot, ChannelType, Option, Permissions, SlashCommandGroup, VoiceChannel
from discord.ext.commands import Cog


# Definitions
class Move(Cog):
    """VC moving commands"""

    # Permissions
    permissions = Permissions()
    permissions.move_members = True


    # Command groups
    command_group = SlashCommandGroup("move", "Commands for moving members in voice channels", guild_only=True, default_member_permissions=permissions)
    command_group_all = command_group.create_subgroup("all", "Move all members in a channel")


    # Commands
    @command_group_all.command()
    async def to(self, ctx: ApplicationContext, channel: Option(VoiceChannel, required=True, description="The channel to move to")): # type: ignore
        """Move all members in the current channel to another one"""

        # Make sure channel is a voice channel
        if channel.type != ChannelType.voice:
            await ctx.response.send_message("The channel must be a voice channel silly")
            return

        # Get current channel
        current_channel = ctx.author.voice.channel

        # Check if channel is None
        if current_channel is None:
            await ctx.response.send_message("You aren't in a VC silly")
            return

        # Check if channels are the same
        if channel == current_channel:
            await ctx.response.send_message("You're already in that VC silly")
            return

        # Send message
        await ctx.response.send_message(f"Moving members from {current_channel.mention} to {channel.mention}...")

        # Move members
        for member in current_channel.members:
            await member.move_to(channel)

        # Edit message
        await ctx.followup.send(f"Moved members from {current_channel.mention} to {channel.mention}")


    @command_group_all.command(name="from")
    async def from_(self, ctx: ApplicationContext, channel: Option(VoiceChannel, required=True, description="The channel to move from")): # type: ignore
        """Move all members in another channel to the current one"""

        # Make sure channel is a voice channel
        if channel.type != ChannelType.voice:
            await ctx.response.send_message("The channel must be a voice channel silly")
            return

        # Get current channel
        current_channel = ctx.author.voice.channel

        # Check if channel is None
        if current_channel is None:
            await ctx.response.send_message("You aren't in a VC silly")
            return

        # Check if channels are the same
        if channel == current_channel:
            await ctx.response.send_message("You cant move from your current channel silly")
            return

        # Send message
        await ctx.response.send_message(f"Moving members from {channel.mention} to {current_channel.mention}...")

        # Move members
        for member in channel.members:
            await member.move_to(current_channel)

        # Edit message
        await ctx.followup.send("Moved members from {channel.mention} to {current_channel.mention}")


def setup(bot: Bot):
    bot.add_cog(Move(bot))
