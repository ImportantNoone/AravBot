# AravBot

discord bot with games and history trivia 

## Features

- **History Trivia**: Test your knowledge with trivia questions about world history
- **Games**:
  - **Higher or Lower**: Guess if the next number is higher or lower
  - **Rock Paper Scissors**: Play against the bot
  - **Number Guessing**: Try to guess the bot's number
- **Leaderboard**: Track scores across your server
- **Customizable prefix**: Change the bot's command prefix

## Requirements

- Python 3.8+
- discord.py
- python-dotenv

## Installation

1. first clone the repository:
```bash
git clone https://github.com/ImportantNoone/AravBot.git
cd AravBot
```

2. install dependencies:
```bash
pip install -r requirements.txt
```

3. create a `.env` file in the root directory:
```
DISCORD_TOKEN=your_bot_token_here
```

4. run the bot:
```bash
python bot.py
```

## commands

### trivia
- `!trivia` - Start a history trivia question
- `!trivia_score` - View your trivia score

### games
- `!rps` - Play rock paper scissors
- `!guess` - Play number guessing game
- `!higher_lower` - Play higher or lower game

### server
- `!leaderboard` - View the server leaderboard
- `!help` - Display all commands

## how to get bot token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Go to the "Bot" tab and click "Add Bot"
4. Under TOKEN, click "Copy"
5. Paste it in your `.env` file

## Invite Bot to Server

1. In Developer Portal, go to OAuth2 > URL Generator
2. Select scopes: `bot`
3. Select permissions: `Send Messages`, `Read Messages/View Channels`, `Manage Messages`
4. Copy the generated URL and open it in your browser

## Contributing

Feel free to fork and submit pull requests with improvements!

## License

MIT License
