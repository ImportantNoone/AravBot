import discord
from discord.ext import commands
import json
import os

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trivia_scores_file = 'data/trivia_scores.json'
        self.game_scores_file = 'data/game_scores.json'
    
    def load_trivia_scores(self):
        if os.path.exists(self.trivia_scores_file):
            with open(self.trivia_scores_file, 'r') as f:
                return json.load(f)
        return {}
    
    def load_game_scores(self):
        if os.path.exists(self.game_scores_file):
            with open(self.game_scores_file, 'r') as f:
                return json.load(f)
        return {}
    
    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx):
        """Display the server leaderboard"""
        trivia_scores = self.load_trivia_scores()
        game_scores = self.load_game_scores()
        
        # Sort trivia scores
        trivia_sorted = sorted(trivia_scores.items(), key=lambda x: x[1], reverse=True)[:10]
        
        embed = discord.Embed(
            title="🏆 AravBot Leaderboard",
            color=discord.Color.gold()
        )
        
        # Trivia leaderboard
        trivia_text = ""
        if trivia_sorted:
            for rank, (user_id, score) in enumerate(trivia_sorted, 1):
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    trivia_text += f"{rank}. {user.mention} - {score} points\n"
                except:
                    trivia_text += f"{rank}. Unknown User - {score} points\n"
        else:
            trivia_text = "No trivia scores yet!"
        
        embed.add_field(
            name="📚 Trivia Leaderboard",
            value=trivia_text,
            inline=False
        )
        
        # Games leaderboard (by total game wins)
        game_totals = {}
        for user_id, games in game_scores.items():
            total = sum(games.values())
            game_totals[user_id] = total
        
        games_sorted = sorted(game_totals.items(), key=lambda x: x[1], reverse=True)[:10]
        
        games_text = ""
        if games_sorted:
            for rank, (user_id, total) in enumerate(games_sorted, 1):
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    games_text += f"{rank}. {user.mention} - {total} wins\n"
                except:
                    games_text += f"{rank}. Unknown User - {total} wins\n"
        else:
            games_text = "No game wins yet!"
        
        embed.add_field(
            name="🎮 Games Leaderboard",
            value=games_text,
            inline=False
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
