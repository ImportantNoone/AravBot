import discord
from discord.ext import commands
import random
import json
import os

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_scores_file = 'data/game_scores.json'
        
        os.makedirs('data', exist_ok=True)
        
        if not os.path.exists(self.game_scores_file):
            with open(self.game_scores_file, 'w') as f:
                json.dump({}, f)
    
    def load_game_scores(self):
        with open(self.game_scores_file, 'r') as f:
            return json.load(f)
    
    def save_game_scores(self, scores):
        with open(self.game_scores_file, 'w') as f:
            json.dump(scores, f, indent=2)
    
    def update_game_score(self, user_id, game_name):
        scores = self.load_game_scores()
        user_id_str = str(user_id)
        
        if user_id_str not in scores:
            scores[user_id_str] = {}
        
        if game_name not in scores[user_id_str]:
            scores[user_id_str][game_name] = 0
        
        scores[user_id_str][game_name] += 1
        self.save_game_scores(scores)
        return scores[user_id_str][game_name]
    
    @commands.command(name='rps')
    async def rock_paper_scissors(self, ctx):
        """Play rock paper scissors against the bot"""
        embed = discord.Embed(
            title="🎮 Rock Paper Scissors",
            description="React with ✊ (rock), ✋ (paper), or ✌️ (scissors)",
            color=discord.Color.purple()
        )
        msg = await ctx.send(embed=embed)
        
        await msg.add_reaction('✊')
        await msg.add_reaction('✋')
        await msg.add_reaction('✌️')
        
        def check(reaction, user):
            return user == ctx.author and reaction.emoji in ['✊', '✋', '✌️']
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            
            choices = {'✊': 'rock', '✋': 'paper', '✌️': 'scissors'}
            player_choice = choices[reaction.emoji]
            bot_choice = random.choice(['rock', 'paper', 'scissors'])
            
            # Determine winner
            if player_choice == bot_choice:
                result = "It's a tie!"
                color = discord.Color.yellow()
            elif (
                (player_choice == 'rock' and bot_choice == 'scissors') or
                (player_choice == 'paper' and bot_choice == 'rock') or
                (player_choice == 'scissors' and bot_choice == 'paper')
            ):
                result = "You win! 🎉"
                color = discord.Color.green()
                self.update_game_score(ctx.author.id, 'rps')
            else:
                result = "I win! 🤖"
                color = discord.Color.red()
            
            result_embed = discord.Embed(
                title="Game Result",
                description=f"You chose: **{player_choice}**\nI chose: **{bot_choice}**\n\n{result}",
                color=color
            )
            await ctx.send(embed=result_embed)
        
        except discord.ext.commands.errors.CommandInvokeError:
            await ctx.send("Game timed out!")
    
    @commands.command(name='guess')
    async def number_guess(self, ctx):
        """Guess the number game (1-100)"""
        number = random.randint(1, 100)
        guesses = 0
        
        embed = discord.Embed(
            title="🔢 Guess the Number",
            description="I'm thinking of a number between 1 and 100. You have 10 guesses!",
            color=discord.Color.teal()
        )
        await ctx.send(embed=embed)
        
        while guesses < 10:
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            
            try:
                msg = await self.bot.wait_for('message', timeout=30.0, check=check)
                
                try:
                    guess = int(msg.content)
                    guesses += 1
                    
                    if guess == number:
                        self.update_game_score(ctx.author.id, 'guess')
                        embed = discord.Embed(
                            title="✅ You got it!",
                            description=f"The number was {number}! You guessed it in {guesses} tries!",
                            color=discord.Color.green()
                        )
                        await ctx.send(embed=embed)
                        return
                    elif guess < number:
                        remaining = 10 - guesses
                        await ctx.send(f"📈 Too low! Guesses remaining: {remaining}")
                    else:
                        remaining = 10 - guesses
                        await ctx.send(f"📉 Too high! Guesses remaining: {remaining}")
                
                except ValueError:
                    await ctx.send("Please enter a valid number!")
                    guesses -= 1
            
            except discord.ext.commands.errors.CommandInvokeError:
                await ctx.send("Game timed out!")
                return
        
        embed = discord.Embed(
            title="❌ Game Over",
            description=f"The number was {number}. Better luck next time!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='higher_lower')
    async def higher_lower(self, ctx):
        """Play higher or lower game"""
        current_number = random.randint(1, 100)
        score = 0
        
        embed = discord.Embed(
            title="📊 Higher or Lower",
            description=f"Current number: **{current_number}**\n\nIs the next number higher or lower? React with ⬆️ (higher) or ⬇️ (lower)",
            color=discord.Color.orange()
        )
        msg = await ctx.send(embed=embed)
        
        await msg.add_reaction('⬆️')
        await msg.add_reaction('⬇️')
        
        while True:
            def check(reaction, user):
                return user == ctx.author and reaction.emoji in ['⬆️', '⬇️']
            
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                
                next_number = random.randint(1, 100)
                player_prediction = 'higher' if reaction.emoji == '⬆️' else 'lower'
                
                # Determine if prediction was correct
                if (player_prediction == 'higher' and next_number > current_number) or \
                   (player_prediction == 'lower' and next_number < current_number):
                    score += 1
                    result = "✅ Correct! +1 point"
                    color = discord.Color.green()
                else:
                    result = "❌ Wrong! Game Over"
                    color = discord.Color.red()
                    self.update_game_score(ctx.author.id, 'higher_lower')
                    
                    result_embed = discord.Embed(
                        title=result,
                        description=f"Previous number: **{current_number}**\nNext number: **{next_number}**\n\n**Final Score: {score}**",
                        color=color
                    )
                    await ctx.send(embed=result_embed)
                    return
                
                current_number = next_number
                
                embed = discord.Embed(
                    title=result,
                    description=f"Current number: **{next_number}**\nScore: **{score}**\n\nIs the next number higher or lower?",
                    color=color
                )
                await msg.edit(embed=embed)
                
                # Remove reactions for next round
                await msg.clear_reactions()
                await msg.add_reaction('⬆️')
                await msg.add_reaction('⬇️')
            
            except:
                await ctx.send("Game timed out!")
                return

async def setup(bot):
    await bot.add_cog(Games(bot))
