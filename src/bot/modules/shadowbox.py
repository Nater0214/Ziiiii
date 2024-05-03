# src/bot/modules/shadowbox.py
# A cog for shadowboxing


# Imports
import asyncio
import math
from random import choice, shuffle

import anytree
from discord import ApplicationContext, Bot, ButtonStyle, Interaction, Member, Option, SlashCommandGroup, TextChannel, ui
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

            self.challenger_move: int = None
            self.opponent_move: int = None
            self.moves: list[int] = []
            self.winner: Member = None


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

            done = self.score in {-3, 3}
            if done:
                if self.score == -3:
                    self.winner = self.challenger
                elif self.score == 3:
                    self.winner = self.opponent
            await interaction.response.edit_message(content=f"{'⬛' if self.challenger_move is None else '🟨'}{'🥊' if self.boxing == self.challenger else '💨'}{self.challenger.mention} {self.emoji_map[self.moves[2]] if self.score <= -3 else '⬛'}{self.emoji_map[self.moves[1]] if self.score <= -2 else '⬛'}{self.emoji_map[self.moves[0]] if self.score <= -1 else '⬛'}⏹{self.emoji_map[self.moves[0]] if self.score >= 1 else '⬛'}{self.emoji_map[self.moves[1]] if self.score >= 2 else '⬛'}{self.emoji_map[self.moves[2]] if self.score >= 3 else '⬛'} {self.opponent.mention}{'🥊' if self.boxing == self.opponent else '💨'}{'⬛' if self.opponent_move is None else '🟨'}", view=self if done else None)


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
        """View for accepting a challenge for anyone"""

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


    class TournamentJoinView(ui.View):
        """View for joining a tournament"""


        # Init
        def __init__(self, cog: Cog, challenger: Member, size: int):
            """Init"""

            # Run super init
            super().__init__()

            # Set cog
            self.cog = cog

            # Set challenger
            self.challenger = challenger

            # Set size
            self.size = size

            # Set player list
            self.player_list: list[str] = []


        async def _run_game(self, node_pair: tuple[anytree.Node, anytree.Node], channel: TextChannel) -> None:
            """Run a game"""

            # Create game view
            game_view = self.cog.GameView(node_pair[0].player, node_pair[1].player)

            # Send message
            await channel.send(f"⬛🥊{node_pair[0].player.mention} ⬛⬛⬛⏹️⬛⬛⬛ {node_pair[1].player.mention}💨⬛", view=game_view)

            # Wait for game to finish
            while game_view.winner is None:
                await asyncio.sleep(1)

            # Update parent node with winner
            if game_view.winner == node_pair[0].player:
                node_pair[0].parent.player = node_pair[0].player
            elif game_view.winner == node_pair[1].player:
                node_pair[1].parent.player = node_pair[1].player
            else:
                raise Exception("Winner not in pair; this should never be run")


        def _make_tournament_tree(self, parent_node: anytree.Node, depth: int) -> anytree.Node:
            """Make the tournament tree and return the base node"""

            # Return if depth is 0
            if depth == 0:
                parent_node.player = self.player_list.pop()

            # Create children
            child_node_1 = anytree.Node("1", parent_node)
            child_node_2 = anytree.Node("2", parent_node)

            # Add grandchildren
            self._make_tournament_tree(child_node_1, depth - 1)
            self._make_tournament_tree(child_node_2, depth - 1)


        async def start(self, channel: TextChannel) -> None:
            """Start the tournament"""

            # Create thread channel
            thread_channel = await channel.create_thread(name=f"{self.challenger.display_name}'s Shadowboxing Tournament")

            # Shuffle player list
            self.player_list = shuffle(self.player_list)

            # Create tournament tree
            base_node = anytree.Node("0")
            self._make_tournament_tree(base_node, math.log2(self.size))

            # Loop until done
            done = False
            current_battles: list[tuple[Member, Member]] = []
            while not done:

                # Get players that need to battle
                node_pairs = [(node.children[0], node.children[1]) for node in anytree.PreOrderIter(base_node) if node.children[0].player is not None and node.children[1].player is not None]

                # Remove battles that are currently happening
                node_pairs = [pair for pair in node_pairs if pair not in current_battles]

                # Create asyncio tasks for battles
                tasks = [asyncio.create_task(self._run_game(pair, thread_channel)) for pair in node_pairs]

                # Run tasks
                for task in tasks:
                    await task


        # Buttons
        @ui.button(label="Join", style=ButtonStyle.green)
        async def join(self, button: ui.Button, interaction: Interaction):
            """Join the tournament"""

            # Make sure the button wasn't pressed by the challenger
            if interaction.user == self.challenger:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You can't join your own tournament silly")
                return

            # Add the user to the player list
            self.player_list.append(interaction.user)

            # Check if tournament is full now
            if len(self.player_list) == self.size:
                button.disabled = True
                await interaction.response.edit_message(content="Tournament is full, starting now", view=None)
                await self.start()


    # Commands
    @command_group.command()
    async def challenge(self, ctx: ApplicationContext, member: Option(Member, description="The member to challenge (don't provide to challenge anyone here)")): # type: ignore
        """Challenge someone to a shadowbox battle"""

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


    # @command_group.command()
    # async def tournament(self, ctx: ApplicationContext, size: Option(int, required=True, description="The size of the tournament, must be a power of 2")): # type: ignore
    #     """Challenge many people to a shadowbox tournament"""

    #     # Make sure size is power of 2
    #     if math.log2(size) % 1 != 0:
    #         await ctx.response.send_message("The size must be a power of 2")
    #         return

    #     # Open accept view
    #     await ctx.response.send_message(f"{ctx.author.mention} started a shadowboxing tournament with a size of {size} players", view=self.TournamentJoinView(self, ctx.author, size))


def setup(bot: Bot):
    bot.add_cog(Shadowbox(bot))
