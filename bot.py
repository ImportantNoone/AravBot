import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up bot with intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load cogs
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename}')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print('------')

@bot.command(name='help')
async def help_command(ctx):
    """Display all available commands"""
    embed = discord.Embed(title='AravBot Commands', color=discord.Color.blue())
    
    embed.add_field(
        name='🎯 Trivia Commands',
        value='`!trivia` - Get a history trivia question\n`!trivia_score` - View your trivia score',
        inline=False
    )
    
    embed.add_field(
        name='🎮 Game Commands',
        value='`!rps` - Play rock paper scissors\n`!guess` - Guess the number game\n`!higher_lower` - Higher or lower game',
        inline=False
    )
    
    embed.add_field(
        name='📊 Server Commands',
        value='`!leaderboard` - View server leaderboard\n`!help` - Show this message',
        inline=False
    )
    
    await ctx.send(embed=embed)

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
