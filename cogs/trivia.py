import discord
from discord.ext import commands
import json
import os
from datetime import datetime

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scores_file = 'data/trivia_scores.json'
        self.questions_file = 'data/history_questions.json'
        self.current_question = {}
        
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        # Load questions
        self.load_questions()
        
        # Initialize scores file
        if not os.path.exists(self.scores_file):
            with open(self.scores_file, 'w') as f:
                json.dump({}, f)
    
    def load_questions(self):
        """Load trivia questions from JSON file"""
        try:
            with open(self.questions_file, 'r') as f:
                self.questions = json.load(f)
        except FileNotFoundError:
            # Default questions if file doesn't exist
            self.questions = [
                {
                    "question": "In what year did the Titanic sink?",
                    "options": ["1912", "1915", "1910", "1920"],
                    "correct": 0
                },
                {
                    "question": "Who was the first President of the United States?",
                    "options": ["Thomas Jefferson", "George Washington", "John Adams", "Benjamin Franklin"],
                    "correct": 1
                },
                {
                    "question": "In what year did World War II end?",
                    "options": ["1943", "1944", "1945", "1946"],
                    "correct": 2
                },
                {
                    "question": "Who wrote the Declaration of Independence?",
                    "options": ["Benjamin Franklin", "Thomas Jefferson", "John Adams", "George Washington"],
                    "correct": 1
                },
                {
                    "question": "In what year did the Roman Empire fall?",
                    "options": ["410 AD", "476 AD", "550 AD", "300 AD"],
                    "correct": 1
                },
                {
                    "question": "Who was the first Emperor of Rome?",
                    "options": ["Julius Caesar", "Augustus", "Nero", "Marcus Aurelius"],
                    "correct": 1
                },
                {
                    "question": "In what year did Christopher Columbus discover America?",
                    "options": ["1490", "1492", "1495", "1500"],
                    "correct": 1
                },
                {
                    "question": "Who was the first person to walk on the moon?",
                    "options": ["Buzz Aldrin", "John Glenn", "Neil Armstrong", "Yuri Gagarin"],
                    "correct": 2
                },
            ]
            self.save_questions()
    
    def save_questions(self):
        """Save questions to JSON file"""
        with open(self.questions_file, 'w') as f:
            json.dump(self.questions, f, indent=2)
    
    def load_scores(self):
        """Load user scores from JSON file"""
        with open(self.scores_file, 'r') as f:
            return json.load(f)
    
    def save_scores(self, scores):
        """Save user scores to JSON file"""
        with open(self.scores_file, 'w') as f:
            json.dump(scores, f, indent=2)
    
    @commands.command(name='trivia')
    async def trivia(self, ctx):
        """Start a history trivia question"""
        if not self.questions:
            await ctx.send("No trivia questions available!")
            return
        
        import random
        question_data = random.choice(self.questions)
        
        self.current_question[ctx.author.id] = {
            'question': question_data,
            'answered': False
        }
        
        embed = discord.Embed(
            title="📚 History Trivia",
            description=question_data['question'],
            color=discord.Color.gold()
        )
        
        for i, option in enumerate(question_data['options'], 1):
            embed.add_field(name=f"Option {i}", value=option, inline=False)
        
        embed.set_footer(text="Reply with the option number (1-4)")
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Handle trivia answers"""
        if message.author == self.bot.user or message.author.bot:
            return
        
        if message.author.id not in self.current_question:
            return
        
        question_data = self.current_question[message.author.id]
        
        if question_data['answered']:
            return
        
        try:
            answer = int(message.content) - 1
            
            if answer < 0 or answer > 3:
                await message.reply("Please enter a number between 1 and 4!")
                return
            
            question_data['answered'] = True
            
            if answer == question_data['question']['correct']:
                # Correct answer
                scores = self.load_scores()
                user_id = str(message.author.id)
                scores[user_id] = scores.get(user_id, 0) + 1
                self.save_scores(scores)
                
                embed = discord.Embed(
                    title="✅ Correct!",
                    description=f"The answer was: {question_data['question']['options'][question_data['question']['correct']]}",
                    color=discord.Color.green()
                )
                embed.set_footer(text=f"Score: {scores[user_id]}")
                await message.reply(embed=embed)
            else:
                # Incorrect answer
                embed = discord.Embed(
                    title="❌ Incorrect!",
                    description=f"The correct answer was: {question_data['question']['options'][question_data['question']['correct']]}",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed)
            
            del self.current_question[message.author.id]
        except ValueError:
            pass
    
    @commands.command(name='trivia_score')
    async def trivia_score(self, ctx):
        """View your trivia score"""
        scores = self.load_scores()
        user_id = str(ctx.author.id)
        score = scores.get(user_id, 0)
        
        embed = discord.Embed(
            title=f"📊 {ctx.author.name}'s Trivia Score",
            description=f"Score: {score}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Trivia(bot))
