# command.py
import asyncio
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from PIL import Image
from io import BytesIO
# from . import model, vision_model, send_question_and_retrieve_result
from app import bot, model,vision_model

# Define button templates
# keyboard_stop = InlineKeyboardMarkup([[InlineKeyboardButton("Stop and reset conversation", callback_data="stop")]])

# Define the main chatbot handler
async def handle_chat_command(client, message):
    """
    Memulai percakapan baru dengan pengguna.

    Argumen:
        message (pyrogram.types.Message): Pesan yang memicu fungsi ini.
    """
    async def get_chat_response(chat, prompt):
        response = chat.send_message(prompt)
        return response.text

    SENDER = message.from_user.id
    MSG_ID = message.chat.id
    
    if len(message.text.split(" ")) < 2:
        return await bot.send_message(MSG_ID, "<b>Gunakan Format : </b>/darmi Pertanyaan")
    
    MSG_TEXT = message.text.split(" ")[1:]
    MSG_TEXT = " ".join(MSG_TEXT)
    
    try:
        chat = model.start_chat(history=[])
        thinking_message = await client.send_message(MSG_ID, "Diterima! aku sedang memikirkan jawabannya...")
        response = await get_chat_response(chat, MSG_TEXT)
        await thinking_message.delete()
        await client.send_message(MSG_ID, response, parse_mode=enums.ParseMode.HTML)

    except asyncio.TimeoutError:
        await client.send_message(MSG_ID, "<b>Percakapan berakhir ✔️</b>\nSudah terlalu lama sejak tanggapan terakhir Anda.", parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        await client.send_message(MSG_ID, "<b>Percakapan berakhir ✔️</b>\nTerjadi masalah.", parse_mode=enums.ParseMode.HTML)

# Register the handler
# handle_chat_command = filters.command("chat")(handle_chat_command)


async def handle_image_command(client, message):
    """
    Menangani perintah /image, di mana bot meminta pengguna untuk mengirim gambar
    dan kemudian memproses gambar menggunakan model visi.

    Argumen:
        message (pyrogram.types.Message): Pesan yang memicu fungsi ini.
    """

    SENDER = message.from_user.id
    MSG_ID = message.chat.id
    
    if not message.reply_to_message.photo:
        return await bot.send_message(MSG_ID, "<b>Gunakan Format : </b>/darma balas gambar")
    
    MSG_TEXT = message.text.strip()
    
    try:
        if message.reply_to_message.photo.file_id:
            thinking_message = await client.send_message(SENDER, "Diterima! aku sedang memikirkan jawabannya...")
            photo_entity = message.reply_to_message.photo.file_id
            photo_path = await client.download_media(photo_entity)
            image = Image.open(photo_path)

            image_buf = BytesIO()
            image.save(image_buf, format="JPEG")
            image_bytes = image_buf.getvalue()

            response = vision_model.generate_content(
                [
                    Part.from_data(image_bytes, mime_type="image/jpeg"),
                    MSG_TEXT,
                ]
            )

            await thinking_message.delete()
            await client.send_message(SENDER, response.text, parse_mode=enums.ParseMode.HTML)

        else:
            pass
            # await client.send_message(SENDER, "Input not valid. Please send me an image after using the /image command.", parse_mode=enums.ParseMode.MARKDOWN)

    except asyncio.TimeoutError:
        await client.send_message(MSG_ID, "<b>Percakapan berakhir ✔️</b>\nSudah terlalu lama sejak tanggapan terakhir Anda.", parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        await client.send_message(MSG_ID, "<b>Percakapan berakhir ✔️</b>\nTerjadi masalah.", parse_mode=enums.ParseMode.HTML)

# Register the handler
# handle_image_command = filters.command("image")(handle_image_command)




@bot.on_message(filters.command("darmi"))
async def handle_chat(client, message):
    await handle_chat_command(client, message)


@bot.on_message(filters.command("darma"))
async def handle_chat(client, message):
    await handle_image_command(client, message)
    
