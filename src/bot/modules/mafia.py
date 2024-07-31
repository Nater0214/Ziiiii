# src/bot/modules/mafia.py
# Commands for the Mafia game


# Imports
from discord import ApplicationContext, ButtonStyle, Interaction, Member, Option, SlashCommandGroup, ui
from discord.ext.commands import Cog


# Definitions
class Mafia(Cog):
    """Mafia commands"""

    # Command group
    command_group = SlashCommandGroup("mafia", "Commands for the Mafia game", guild_only=True, guild_ids=1235772100384526377)


    # Views
    class JoinView(ui.View):
        """The view for joining the game"""


        def __init__(self, cog: Cog, author: Member):
            """Init"""

            # Run super init
            super().__init__()

            # Set cog
            self.cog = cog

            # Set author
            self.author = author

            # Set player list
            self.player_list: list[str] = []


            # Buttons
            @ui.button(label="Join", style=ButtonStyle.blurple)
            async def join(self, button: ui.Button, interaction: Interaction):
                """Join the Mafia game"""


    # Commands
    @command_group.command()
    async def start(self, ctx: ApplicationContext, anonymous: Option(bool, default=False, description="Whether all players are anonymous"), blind_mafia: Option(bool, required=True, description="Whether the mafia members can see each other")): # type: ignore
        """Start a mafia game where everyone can join"""