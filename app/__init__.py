import asyncio
from pyrogram import filters, Client

from pyromod import listen
from app.config import *
from app.database import udb, load_data_json

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="ubot",
            api_hash=API_HASH,
            api_id=API_ID,
            bot_token=BOT_TOKEN,
            device_model="IPHONE 30 PROMAXXXWIN",
        )

    async def start(self):
        await super().start()
        

    async def stop(self, *args):
        await super().stop()

bot = Bot()





