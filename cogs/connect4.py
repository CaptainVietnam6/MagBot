import discord
from discord.ext import commands
import asyncio

import numpy as np


def auto_color(ctx):
    roles = (ctx.message.guild.get_member(ctx.me.id)).roles 
    roles.reverse()
    return roles[0].color

class Connect4Game:
    
    ROW_COUNT = 6
    COLUMN_COUNT = 7
    WHITE_BACKGROUND = '⚪'
    YELLOW_BLOCK = '🟡'
    RED_BLOCK = '🔴'
    WIDTH = 6
    LENGTH = 7

    def __init__(self):
        board = np.zeros((self.WIDTH, self.LENGTH), dtype=str)
        for i in range(len(board)):
            for j in range(len(board[i])):
                board[i][j] = self.WHITE_BACKGROUND
        self.board = board
        self.accept = True
        self.over = False
        self.turn = 1

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def display_board(self):
        board, output = np.flip(self.board, 0), ''
        for item in board:
            for i in range(len(item)):
                output += f'{item[i]} ' 
            output += '\n'
        for item in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']:
            output += f'{item} '
        return output

    def is_valid_location(self, col):
        return self.board[5][col] == self.WHITE_BACKGROUND

    def get_next_open_row(self, col):
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == self.WHITE_BACKGROUND:
                return r

    def winning_move(self, piece):
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    self.over = True
                    return True

        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    self.over = True
                    return True

        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    self.over = True
                    return True

        for c in range(self.COLUMN_COUNT-3):
            for r in range(3, self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    self.over = True
                    return True

class Connect4(commands.Cog):
    def __init__(self, client):
        self.client = client

    # CONNECT4 
    @commands.command()
    async def connect4(self, ctx, user):
        
        initiator, challenged = ctx.message.author, await discord.ext.commands.MemberConverter().convert(ctx, user)
        designer = await discord.ext.commands.MemberConverter().convert(ctx, '597621743070216203')
        game = Connect4Game()

        def game_board(display_turn = False):
            if display_turn is False:
                embed = discord.Embed(title = f'', description = f'{game.display_board()}', color = auto_color(ctx))
            else: embed = discord.Embed(title = f'Turn {str(game.turn)}', description = f'{game.display_board()}', color = auto_color(ctx))
            return embed.set_footer(text = 'Designed by Junle', icon_url = designer.avatar_url)

        async def edit_game_embed(msg, color = None):
            if color == None:
                await msg.edit(content = f'🟡 {initiator.mention}\n🔴 {challenged.mention}\n——————————', embed = game_board(True))
            else:
                if color == 'yellow':
                    embed = discord.Embed(title = f'Turn {str(game.turn)}', description = f'{game.display_board()}', color = discord.Color.gold())
                else:
                    embed = discord.Embed(title = f'Turn {str(game.turn)}', description = f'{game.display_board()}', color = discord.Color.red())
                await msg.edit(content = f'🟡 {initiator.mention}\n🔴 {challenged.mention}\n——————————', embed = embed.set_footer(text = 'Designed by Junle', icon_url = designer.avatar_url))
        
        embed = game_board()
        embed.set_footer(text = 'Designed by Junle', icon_url = designer.avatar_url)
        board = await ctx.send(content = f'{initiator.mention} challenged {challenged.mention} to a duel!', embed = embed)

        for emoji in ['✅', '❌']:
            await board.add_reaction(emoji)

        def check_for_red(reaction, user):
            return reaction.message.id == board.id and user.id == challenged.id

        def check_for_yellow(reaction, user):
            return reaction.message.id == board.id and user.id == initiator.id

        while True:
            try: 
                reaction, _ = await self.client.wait_for("reaction_add", timeout = 15, check = check_for_red)
                if str(reaction.emoji) == '✅':
                    await edit_game_embed(board, 'yellow'); await board.clear_reactions(); break
                    start_game = True; return start_game
                if str(reaction.emoji) == '❌': await board.delete(); game.accept = False; break
            except asyncio.TimeoutError: await board.delete(); game.accept = False; break

        for emoji in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']:
            await board.add_reaction(emoji)
        emoji_dict = {'1️⃣': 0, '2️⃣': 1, '3️⃣': 2, '4️⃣': 3, '5️⃣': 4, '6️⃣': 5, '7️⃣': 6}

        while game.accept:
            try: 
                if game.turn - 1 >= game.WIDTH * game.LENGTH: break
                while True:
                    reaction, _ = await self.client.wait_for("reaction_add", timeout = 60, check = check_for_yellow)
                    col = emoji_dict[reaction.emoji]
                    if game.is_valid_location(col): 
                        row = game.get_next_open_row(col)
                        game.drop_piece(row, col, game.YELLOW_BLOCK)
                        break
                if game.winning_move(game.YELLOW_BLOCK): 
                    final_embed = discord.Embed(title = f'Turn {str(game.turn)}', description = f'{game.display_board()}', color = discord.Color.gold())
                    final_embed.set_footer(text = 'Designed by Junle', icon_url = designer.avatar_url)
                    await board.edit(content = f'👑 **Winner:**\n🟡 {initiator.mention}\n——————————\n🔴 {challenged.mention}', embed = final_embed)
                    break
                game.turn += 1
                await edit_game_embed(board, 'red')

                if game.turn - 1 >= game.WIDTH * game.LENGTH: break
                while True:
                    reaction, _ = await self.client.wait_for("reaction_add", timeout = 60, check = check_for_red)
                    col = emoji_dict[reaction.emoji]
                    if game.is_valid_location(col): 
                        row = game.get_next_open_row(col)
                        game.drop_piece(row, col, game.RED_BLOCK)
                        break
                if game.winning_move(game.RED_BLOCK): 
                    final_embed = discord.Embed(title = f'Turn {str(game.turn)}', description = f'{game.display_board()}', color = discord.Color.gold())
                    final_embed.set_footer(text = 'Designed by Junle', icon_url = designer.avatar_url)
                    await board.edit(content = f'👑 **Winner:**\n🔴 {challenged.mention}\n——————————\n🟡 {initiator.mention}', embed = final_embed)
                    break
                game.turn += 1
                await edit_game_embed(board, 'yellow')

            except asyncio.TimeoutError: await ctx.send('Timeout!') ; await board.delete(); break
        
def setup(client):
    client.add_cog(Connect4(client))