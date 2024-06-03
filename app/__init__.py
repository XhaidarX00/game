import asyncio
from pyrogram import filters, Client
# from pyrogram.types import CallbackQuery
# import vertexai
# from vertexai.generative_models._generative_models import HarmCategory, HarmBlockThreshold
# from vertexai.preview.generative_models import GenerativeModel

from pyromod import listen
from app.config import *
from app.database import udb, load_data_json

# # Initialize Vertex AI with project and location
# vertexai.init(project=project_id, location=location)

# # Configuration settings for the generative model
# generation_config = {
#     "temperature": 0.7,
#     "top_p": 1,
#     "top_k": 1,
#     "max_output_tokens": 2048,
# }

# # Safety settings to control harmful content blocking thresholds
# safety_settings = {
#     HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
#     HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
#     HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
#     HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
# }

# # Initialize generative models
# model = GenerativeModel("gemini-pro", generation_config=generation_config, safety_settings=safety_settings)
# vision_model = GenerativeModel("gemini-pro-vision", generation_config=generation_config, safety_settings=safety_settings)



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




# # Define helper function to retrieve a message from a conversation and handle button clicks
# async def send_question_and_retrieve_result(prompt, message, client, keyboard):
#     """
#     Sends a question to the user and retrieves their response.

#     Args:
#         prompt (str): The question to ask the user.
#         message (pyrogram.types.Message): The message object to use for sending the message.
#         keyboard (list): The keyboard to send with the message.

#     Returns:
#         pyrogram.types.Message or None: The user's response or None if they tapped a button.
#     """
#     sent_message = await message.reply(prompt, reply_markup=keyboard)
#     response = None

#     def stop_callback(client, callback_query):
#         nonlocal response
#         response = callback_query
#         return True

#     client.add_handler(filters.CallbackQuery("stop")(stop_callback))

#     while response is None:
#         try:
#             response = await client.listen(message.chat.id, timeout=600)
#         except asyncio.TimeoutError:
#             await sent_message.delete()
#             return None

#     await sent_message.delete()
#     if isinstance(response, CallbackQuery):
#         await response.message.delete()
#         return None
#     else:
#         return response





