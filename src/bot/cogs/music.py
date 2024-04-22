# src/bot/cogs/mc.py
# A cog for music related commands


# Imports
import os

from discord import ApplicationContext, Bot, ButtonStyle, FFmpegPCMAudio, HTTPException, Interaction, Option, SlashCommandGroup, ui
from discord.ext.commands import Cog

from src import audio


# Definitions
class Music(Cog):
    """Music commands"""
    
    # Command group
    command_group = SlashCommandGroup("music", "Music commands", guild_only=True)
    
    
    # Views
    class PlaySongView(ui.View):
        """A view for playing a single song"""
        
        def __init__(self, song_name: str, download_link: str) -> None:
            """Init"""
            
            # Run super init
            super().__init__()
            
            # Create the button
            button = ui.Button(label="Play", style=ButtonStyle.blurple)
            button.callback = self.play_song
            self.add_item(button)
            
            # Set song name
            self.song_name = song_name
            
            # Set download link
            self.download_link = download_link
        
        # Button method
        async def play_song(self, interaction: Interaction):
            """Play the song"""
            
            # Send the status message
            await interaction.response.edit_message(content=f"Playing {self.song_name}", view=None)
            
            # Get the audio source
            audio_source = FFmpegPCMAudio(self.download_link, **{'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-n'}, executable=".\\ffmpeg.exe" if os.name == "nt" else "ffmpeg")
            
            # Play the audio
            interaction.guild.voice_client.play(audio_source)
    
    
    class ResultSelectView(ui.View):
        """A view for selecting a song"""
        
        def __init__(self, query_results: list[str], download_links: list[str]) -> None:
            """Init"""
            
            # Run super init
            super().__init__()
            
            # Create the buttons
            for num, result in enumerate(query_results):
                button = ui.Button(label=str(num + 1), style=ButtonStyle.blurple, custom_id=str(num))
                button.callback = self.play_song
                self.add_item(button)
            
            # Associate each song with a number
            self.song_nums = {str(num): result for num, result in enumerate(query_results)}
            
            # Associate each download link with a number
            self.download_links = {str(num): link for num, link in enumerate(download_links)}
        
        # Button method
        async def play_song(self, interaction: Interaction):
            """Play the selected song"""
            
            # Send the status message
            await interaction.response.edit_message(content=f"Playing *{self.song_nums[interaction.custom_id]}*", view=None)
            
            # Get the audio source
            audio_source = FFmpegPCMAudio(self.download_links[interaction.custom_id], **{'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-n'}, executable=".\\ffmpeg.exe" if os.name == "nt" else "ffmpeg")
            
            # Play the audio
            interaction.guild.voice_client.play(audio_source)
    
    
    # Commands
    @command_group.command(guild_only=True)
    async def search(self, ctx: ApplicationContext, source: Option(str, choices=["kevin", "ncs", "url"], description="The source of the song"), query: Option(str, description="The query used to find the song")): # type: ignore
        """Play a song from a source by a query"""
        
        try:
            # Do stuff based on voice state
            if ctx.guild.voice_client is None:
                if ctx.user.voice is not None:
                    await ctx.user.voice.channel.connect()
                else:
                    await ctx.response.send_message("You aren't in a VC dumbass")
                    return
            else:
                if ctx.guild.voice_client.is_playing():
                    await ctx.response.send_message("I'm busy playing a song rn sorry")
                    return
                elif ctx.guild.voice_client.channel != ctx.user.voice.channel:
                    await ctx.response.send_message("I'm busy with someone else rn sorry")
                    return
            
            # Acknowledge the command
            await ctx.defer()
            
            # Get the query results
            query_results, download_links = audio.search_song(source, query)
            
            # Respond appropriately
            if len(query_results) > 10:
                await ctx.followup.send("I found too many")
            elif len(query_results) > 1:
                await ctx.followup.send("\n".join([f"I found {len(query_results)} songs:", *[f'{num}. *{song}*' for num, song in enumerate(query_results)]]), view=self.ResultSelectView(query_results, download_links))
            elif len(query_results) == 1:
                await ctx.followup.send(f"I found *{query_results[0]}*", view=self.PlaySongView(query_results[0], download_links[0]))
            else:
                await ctx.followup.send("I found nothing :/")
            
        except HTTPException:
            try:
                await ctx.guild.voice_client.disconnect()
            except AttributeError:
                pass
    
    
    @command_group.command(guild_only=True)
    async def stop(self, ctx: ApplicationContext, disconnect: Option(bool, description="Wether I should disconnect from the vc") = False): # type: ignore
        """Stop a playing song"""
        
        # Do stuff based on voice state
        if ctx.guild.voice_client is None:
            await ctx.response.send_message("I'm not even in a vc")
        else:
            if ctx.guild.voice_client.is_playing():
                ctx.guild.voice_client.stop()
                if disconnect:
                    await ctx.guild.voice_client.disconnect()
                    await ctx.response.send_message("Bye")
                else:
                    await ctx.response.send_message("Stopped")
            elif ctx.guild.voice_client.channel != ctx.user.voice.channel:
                await ctx.response.send_message("You're in a different vc!")
            elif disconnect:
                await ctx.guild.voice_client.disconnect()
                await ctx.response.send_message("Bye")


def setup(bot: Bot):
    bot.add_cog(Music(bot))
