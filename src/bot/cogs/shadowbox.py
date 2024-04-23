# src/bot/cogs/shadowbox.py
# A cog for shadowboxing


# Imports
from random import choice

from discord import ApplicationContext, Bot, ButtonStyle, Interaction, Member, Option, SlashCommandGroup, ui
from discord.ext.commands import Cog
from naters_utils.iterables import NoneList


# Definitions
class Shadowbox(Cog):
    """Shadowbox commands"""
    
    # Command group
    command_group = SlashCommandGroup("shadowbox", "Commands for shadowboxing", guild_only=True)
    
    
    # Views
    class SelfGameView(ui.View):
        """View for starting a shadowbox game"""
        
        # Emoji map
        emoji_map = {
            0: "⬆️",
            2: "⬇️",
            3: "⬅️",
            1: "➡️"
        }
        
        # Init
        def __init__(self, challenger: Member, bot: Member) -> None:
            """Init"""
            
            # Run super init
            super().__init__()
            
            # Add buttons
            self.up_button = ui.Button(label=self.emoji_map[0], style=ButtonStyle.gray)
            self.down_button = ui.Button(label=self.emoji_map[2], style=ButtonStyle.gray)
            self.left_button = ui.Button(label=self.emoji_map[3], style=ButtonStyle.gray)
            self.right_button = ui.Button(label=self.emoji_map[1], style=ButtonStyle.gray)
            
            self.up_button.callback = self.up
            self.down_button.callback = self.down
            self.left_button.callback = self.left
            self.right_button.callback = self.right
            
            self.add_item(self.up_button)
            self.add_item(self.down_button)
            self.add_item(self.left_button)
            self.add_item(self.right_button)
            
            # Set challenger
            self.challenger = challenger
            
            # Set opponent
            self.opponent = bot
            
            # Setup game
            self.score = 0
            self.boxing = self.challenger
            
            self.challenger_move = None
            self.moves = NoneList(3)
        
        # Button methods
        async def up(self, interaction: Interaction):
            """User played up"""
            
            # Set player move
            if interaction.user == self.challenger:
                self.challenger_move = 0
            else:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You aren't in this game silly")
                return
            
            await self.scoring(interaction)
        
        
        async def down(self, interaction: Interaction):
            """User played down"""
            
            # Set player move
            if interaction.user == self.challenger:
                self.challenger_move = 2
            else:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You aren't in this game silly")
                return
            
            await self.scoring(interaction)
        
        
        async def left(self, interaction: Interaction):
            """User played left"""
            
            # Set player move
            if interaction.user == self.challenger:
                self.challenger_move = 3
            else:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You aren't in this game silly")
                return
            
            await self.scoring(interaction)
        
        
        async def right(self, interaction: Interaction):
            """User played right"""
            
            # Set player move
            if interaction.user == self.challenger:
                self.challenger_move = 1
            else:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You aren't in this game silly")
                return
            
            await self.scoring(interaction)
        
        
        # Methods
        async def scoring(self, interaction: Interaction) -> None:
            """Do scoring"""
            
            # Bot makes a move
            opponent_move = choice([move for move in [0, 2, 3, 1] if move not in self.moves])
            
            # Check if moves are the same
            if self.challenger_move == opponent_move:
                # Change score accordingly
                if self.boxing == self.challenger:
                    self.score -= 1
                elif self.boxing == self.opponent:
                    self.score += 1
                
                # Add to moves list
                self.moves.append(self.challenger_move)
                
                # Disable button
                match self.challenger_move:
                    case 0:
                        self.up_button.disabled = True
                    case 2:
                        self.down_button.disabled = True
                    case 3:
                        self.left_button.disabled = True
                    case 1:
                        self.right_button.disabled = True
            else:
                # Set score to 0
                self.score = 0
                
                # Reset moves list
                self.moves.clear()
                
                # Enable all buttons
                self.up_button.disabled = False
                self.down_button.disabled = False
                self.left_button.disabled = False
                self.right_button.disabled = False
                
                # Set other player to boxing
                if self.boxing == self.challenger:
                    self.boxing = self.opponent
                elif self.boxing == self.opponent:
                    self.boxing = self.challenger
            
            # Reset player moves
            self.challenger_move = None
            opponent_move = None
            
            await interaction.response.edit_message(content=f"{'⬛' if self.challenger_move is None else '🟨'}{'🥊' if self.boxing == self.challenger else '💨'}{self.challenger.mention} {self.emoji_map[self.moves[2]] if self.score <= -3 else '⬛'}{self.emoji_map[self.moves[1]] if self.score <= -2 else '⬛'}{self.emoji_map[self.moves[0]] if self.score <= -1 else '⬛'}⏹️{self.emoji_map[self.moves[0]] if self.score >= 1 else '⬛'}{self.emoji_map[self.moves[1]] if self.score >= 2 else '⬛'}{self.emoji_map[self.moves[2]] if self.score >= 3 else '⬛'} {self.opponent.mention}{'🥊' if self.boxing == self.opponent else '💨'}🟨", view=self if self.score not in [-3, 3] else None)
    
    class GameView(ui.View):
        """View for starting a shadowbox game"""
        
        # Emoji map
        emoji_map = {
            0: "⬆️",
            2: "⬇️",
            3: "⬅️",
            1: "➡️"
        }
        
        # Init
        def __init__(self, challenger: Member, opponent: Member) -> None:
            """Init"""
            
            # Run super init
            super().__init__()
            
            # Add buttons
            self.up_button = ui.Button(label=self.emoji_map[0], style=ButtonStyle.gray)
            self.down_button = ui.Button(label=self.emoji_map[2], style=ButtonStyle.gray)
            self.left_button = ui.Button(label=self.emoji_map[3], style=ButtonStyle.gray)
            self.right_button = ui.Button(label=self.emoji_map[1], style=ButtonStyle.gray)
            
            self.up_button.callback = self.up
            self.down_button.callback = self.down
            self.left_button.callback = self.left
            self.right_button.callback = self.right
            
            self.add_item(self.up_button)
            self.add_item(self.down_button)
            self.add_item(self.left_button)
            self.add_item(self.right_button)
            
            # Set challenger
            self.challenger = challenger
            
            # Set opponent
            self.opponent = opponent
            
            # Setup game
            self.boxing = challenger
            self.score = 0
            
            self.challenger_move = None
            self.opponent_move = None
            self.moves = []
        
        
        # Button methods
        async def up(self, interaction: Interaction):
            """User played up"""
            
            # Set player move
            if interaction.user == self.challenger:
                self.challenger_move = 0
            elif interaction.user == self.opponent:
                self.opponent_move = 0
            else:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You aren't in this game silly")
                return
            
            await self.scoring(interaction)
        
        
        async def right(self, interaction: Interaction):
            """User played right"""
            
            # Set player move
            if interaction.user == self.challenger:
                self.challenger_move = 1
            elif interaction.user == self.opponent:
                self.opponent_move = 1
            else:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You aren't in this game silly")
                return
            
            await self.scoring(interaction)
        
        
        async def down(self, interaction: Interaction):
            """User played down"""
            
            # Set player move
            if interaction.user == self.challenger:
                self.challenger_move = 2
            elif interaction.user == self.opponent:
                self.opponent_move = 2
            else:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You aren't in this game silly")
                return
            
            await self.scoring(interaction)
        
        
        async def left(self, interaction: Interaction):
            """User played left"""
            
            # Set player move
            if interaction.user == self.challenger:
                self.challenger_move = 3
            elif interaction.user == self.opponent:
                self.opponent_move = 3
            else:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You aren't in this game silly")
                return
            
            await self.scoring(interaction)
        
        
        # Methods
        async def scoring(self, interaction: Interaction) -> None:
            """Do scoring"""
            
            # Check if both players have made a move
            if self.challenger_move is None or self.opponent_move is None:
                pass
            
            else:
                # Check if moves are the same
                if self.challenger_move == self.opponent_move:
                    # Change score accordingly
                    if self.boxing == self.challenger:
                        self.score -= 1
                    elif self.boxing == self.opponent:
                        self.score += 1
                    
                    # Add to moves list
                    self.moves.append(self.challenger_move)
                    
                    # Disable button
                    match self.challenger_move:
                        case 0:
                            self.up_button.disabled = True
                        case 1:
                            self.right_button.disabled = True
                        case 2:
                            self.down_button.disabled = True
                        case 3:
                            self.left_button.disabled = True
                else:
                    # Set score to 0
                    self.score = 0
                    
                    # Reset moves list
                    self.moves.clear()
                    
                    # Enable all buttons
                    self.up_button.disabled = False
                    self.down_button.disabled = False
                    self.left_button.disabled = False
                    self.right_button.disabled = False
                    
                    # Set other player to boxing
                    if self.boxing == self.challenger:
                        self.boxing = self.opponent
                    elif self.boxing == self.opponent:
                        self.boxing = self.challenger
                
                # Reset player moves
                self.challenger_move = None
                self.opponent_move = None
            
            await interaction.response.edit_message(content=f"{'⬛' if self.challenger_move is None else '🟨'}{'🥊' if self.boxing == self.challenger else '💨'}{self.challenger.mention} {self.emoji_map[self.moves[2]] if self.score <= -3 else '⬛'}{self.emoji_map[self.moves[1]] if self.score <= -2 else '⬛'}{self.emoji_map[self.moves[0]] if self.score <= -1 else '⬛'}⏹{self.emoji_map[self.moves[0]] if self.score >= 1 else '⬛'}{self.emoji_map[self.moves[1]] if self.score >= 2 else '⬛'}{self.emoji_map[self.moves[2]] if self.score >= 3 else '⬛'} {self.opponent.mention}{'🥊' if self.boxing == self.opponent else '💨'}{'⬛' if self.opponent_move is None else '🟨'}", view=self if self.score not in [-3, 3] else None)
    
    
    class AcceptView(ui.View):
        """View for accepting a challenge"""
        
        # Init
        def __init__(self, cog: Cog, challenger: Member, opponent: Member):
            """Init"""
            
            # Run super init
            super().__init__()
            
            # Set cog
            self.cog = cog
            
            # Set challenger
            self.challenger = challenger
            
            # Set opponent
            self.opponent = opponent
        
        
        # Buttons
        @ui.button(label="Accept", style=ButtonStyle.green)
        async def accept(self, button: ui.Button, interaction: Interaction):
            """Accept the challenge"""
            
            # Make sure the button was clicked by the challenged user
            if interaction.user != self.opponent:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You weren't the one challenged silly")
                return
            
            await interaction.response.edit_message(content=f"⬛🥊{self.challenger.mention} ⬛⬛⬛⏹️⬛⬛⬛ {self.opponent.mention}💨⬛", view=self.cog.GameView(self.challenger, self.opponent))
        
        
        @ui.button(label="Decline", style=ButtonStyle.red)
        async def decline(self, button: ui.Button, interaction: Interaction):
            """Decline the challenge"""
            
            # Make sure the button was clicked by the challenged user
            if interaction.user != self.opponent:
                await interaction.user.send(f"{interaction.message.jump_url}\n↘>>>You weren't the one challenged silly")
                return
            
            await interaction.response.edit_message(content="Yikes", view=None)
    
    
    class AcceptAnyoneView(ui.View):
        
        
        # Init
        def __init__(self, cog: Cog, challenger: Member):
            """Init"""
            
            # Run super init
            super().__init__()
            
            # Set cog
            self.cog = cog
            
            # Set challenger
            self.challenger = challenger
        
        
        # Buttons
        @ui.button(label="Accept", style=ButtonStyle.green)
        async def accept(self, button: ui.Button, interaction: Interaction):
            """Accept the challenge"""
            
            # Make sure the button wasn't clicked by the challenger
            if interaction.user == self.challenger:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You can't accept your own challenge silly")
                return
            
            await interaction.response.edit_message(content=f"⬛🥊{self.challenger.mention} ⬛⬛⬛⏹️⬛⬛⬛ {interaction.user.mention}💨⬛", view=self.cog.GameView(self.challenger, interaction.user))
    
    
    # Commands
    @command_group.command()
    async def challenge(self, ctx: ApplicationContext, member: Option(Member, required=False, description="The member to challenge (don't provide to challenge anyone here)")): # type: ignore
        """Challenge someone to a shadowbox game"""
        
        match member:
            
            # User challenged themselves
            case ctx.author:
                await ctx.response.send_message("You can't challenge yourself")
            
            # User challenged the bot
            case ctx.bot.user:
                await ctx.response.send_message(f"⬛🥊{ctx.author.mention} ⬛⬛⬛⏹️⬛⬛⬛ {ctx.bot.user.mention}💨🟨", view=self.SelfGameView(ctx.author, ctx.bot.user))
            
            # User challenged no one
            case None:
                await ctx.response.send_message(f"{ctx.author.mention} challenged anyone @here to a shadowbox battle\nThe first to accept will be put in the battle", view=self.AcceptAnyoneView(self, ctx.author))
            
            # User challenged another member
            case _:
                await ctx.response.send_message(f"{ctx.author.mention} challenged {member.mention} to a shadowbox battle", view=self.AcceptView(self, ctx.author, member))


def setup(bot: Bot):
    bot.add_cog(Shadowbox(bot))
