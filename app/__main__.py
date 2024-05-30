# __main__.py
import asyncio
from pyrogram import *
# from .command import handle_chat_command, handle_image_command, handle_start_command
from app import bot
from app.src.core.plugins import loadPlugins

# Configure Pyrogram client
# client = Client(config.session_name_bot, api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

# Register command handlers
# client.add_handler(handle_chat_command)
# client.add_handler(handle_image_command)
# client.add_handler(handle_start_command)

loop = asyncio.get_event_loop_policy()
event_loop = loop.get_event_loop()

async def main(): 
    await asyncio.gather(bot.start())
    await asyncio.gather(loadPlugins(), idle())



if __name__ == "__main__":
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(main())