from pyrogram import *
from app.config import *
# from pytgcalls import PyTgCalls

class UbotNc(Client):
    __module__ = "pyrogram.client"
    _ubot = []
    _prefix = {}
    _get_my_id = []
    _translate = {}
    _get_my_peer = {}

    def __init__(self, api_id, api_hash, device_model="Dubot", **kwargs):
        super().__init__(**kwargs)
        self.api_id = api_id
        self.api_hash = api_hash
        self.device_model = device_model
        # self.call_py = PyTgCalls(self)

    def on_message(self, filters=filters.Filter):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters))
            return func

        return decorator
        
    def set_prefix(self, user_id, prefix):
        self._prefix[user_id] = prefix

    async def start(self):
        await super().start()
        # await self.call_py.start()
        self._prefix[self.me.id] = ["."]
        self._ubot.append(self)
        self._get_my_id.append(self.me.id)
        self._translate[self.me.id] = "id"
        print(f"Starting Userbot ({self.me.id}|{self.me.first_name})")


ubot = UbotNc(
    name="ubot1",
    api_id=API_ID,
    api_hash=API_HASH,
    device_model="Dubot",
)