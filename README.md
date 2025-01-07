# Telegram Bot: Multi-Game Categories

This repository contains a Telegram bot built using Python and the `pyrogram` library, integrated with a Redis database. The bot combines multiple game categories into one flexible and comprehensive bot, providing users with a variety of game options.

## Game Categories

The bot includes the following game categories:

- **ASAH OTAK**
- **TEKA-TEKI**
- **FAMILY 100**
- **SUSUN KATA**
- **TEBAK GAMBAR**
- **SIAPAKAH AKU?**
- **TEBAK - TEBAKAN**
- **TEBAKAN CAK LONTONG**

## Features

- **Integrated Games**: Combines multiple Telegram game bots into a single bot.
- **Flexible Configuration**: Allows for easy customization of Redis and bot settings.
- **Redis Integration**: Efficiently handles game state and user data.

## Prerequisites

- Python 3.8+
- Redis database (hosted locally or in the cloud)

## Configuration

To set up the bot, you need to configure the following variables:

```python
# Redis Configuration
redis_host = 
redis_port = 
redis_password = 

# Bot Configuration
session_name_bot = 'haidar_multi_game_bot'
API_ID =
API_HASH = 
BOT_TOKEN = 
OWNER_ID = 
```

Replace the Redis credentials and bot API keys with your own configuration.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/multi-game-bot.git
   cd multi-game-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the bot:
   ```bash
   python bot.py
   ```

## Deployment

The bot can be deployed on any VPS or cloud instance. Use tools like `systemd` or `pm2` to keep the bot running continuously.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
