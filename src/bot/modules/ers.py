# src/bot/cogs/ers.py
# ERS commands


# Imports
from typing import Any

from discord import ApplicationContext, Bot, ButtonStyle, Cog, Interaction, Member, Option, SlashCommandGroup, ui


# Definitions
class ERS(Cog):
    """ERS card game commands"""

    # Command group
    command_group = SlashCommandGroup("ers", "Commands for the ERS card game", guild_only=True)


    # Views
    class JoinView(ui.View):

        # Init
        def __init__(self, cog: Cog, author: Member, max_players: int, settings: dict[str, Any]) -> None:
            """Init"""

            # Run super init
            super().__init__(timeout=1800)

            # Set cog
            self.cog = cog

            # Set author
            self.author = author

            # Set max players
            self.max_players = max_players

            # Set settings
            self.settings = settings

            # Set player list
            self.player_list: list[Member] = [author]

        @ui.button(label="Join", style=ButtonStyle.green)
        async def join(self, button: ui.Button, interaction: Interaction):
            """Join the game"""

            # Check if user is already in the game
            if interaction.user in self.player_list:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You're already in this game silly")
            
            # Add user to game
            self.player_list.append(interaction.user)

            # Disable button if max players reached
            if len(self.player_list) >= self.max_players:
                button.disabled = True

            # Add player to message
            await interaction.response.edit_message(content=f"{self.author.mention} created an ERS game with a max of {self.max_players} players\nPlayers in game:\n{'\n'.join(self.player_list)}")


        
        @ui.button(label="Start", style=ButtonStyle.gray)
        async def start(self, button: ui.Button, interaction: Interaction):
            """Start the game"""

            # Make sure user is the author of the game
            if interaction.user != self.author:
                interaction.user.send(f"{interaction.message.jump_url}\n>>>You aren't the author of this game; you can't start it!")
            
            await interaction.response.edit_message(content="Starting game...")


    # Commands
    @command_group.command()
    async def create(self, ctx: ApplicationContext, max_players: Option(int, default=8, description="The maximum players in the game"), slap_in: Option(bool, default=True, description="Whether players can slap back into the game after going out"), decks: Option(int, default=1, description="The number of card decks to use (I recommend more than one for big games)"), jokers_per_deck: Option(int, default=2, description="The number of jokers in each deck")): # type: ignore
        """Create an ERS game"""

        # Check if max players is less than 2
        if max_players < 2:
            await ctx.response.send_message("You can't have a game with less than 2 people!")
            return

        # Check if decks is less than 1
        if decks < 1:
            await ctx.response.send_message("You can't have a game with less than 1 decks!")
            return

        # Check if jokers amount of negative
        if jokers_per_deck < 0:
            await ctx.response.send_message("You can't have negative jokers per deck!")
            return

        await ctx.response.send_message(f"{ctx.author.mention} created an ERS game with a max of {max_players} players\nPlayers in game:\n{ctx.author.mention}", view=self.JoinView(self, ctx.author, max_players, {"slap_in": slap_in, "decks": decks, "jokers_per_deck": jokers_per_deck}))


def setup(bot: Bot):
    bot.add_cog(ERS(bot))