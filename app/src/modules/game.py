from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import Client, filters, enums
from app import bot, OWNER_ID, udb
from app.src.helpers.parser import mention_html
from app.database.dbgame import DBGAME


# Menampilkan List Tagall
@bot.on_message(filters.command("ppplay"))
async def convertascci(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.from_user.first_name
    if message.from_user.last_name:
        nama += f" {message.from_user.last_name}"
    
    message_text, keyboard = send_categories()
    user_mention_display = await mention_html(name, user_id)
    text = f"Hai 👋 {user_mention_display}\n"
    text += message_text
    await client.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Daftar kategori Game
categories = [
    "TEBAKAN CAK LONTONG"
]


# Fungsi untuk mengirim daftar kategori
def send_categories(page=0, per_page=4):
    keyboard = []
    text = "\n"
    index_count = 0
    # Tentukan batasan halaman
    start_index = page * per_page
    end_index = min(start_index + per_page, len(categories))
    for idx in range(start_index, end_index, 2):
        text += f"{idx + 1}. {categories[idx]}\n"
        row = [InlineKeyboardButton(str(idx + 1), callback_data=f"category_{idx}")]
        if idx + 1 < end_index:
            row.append(InlineKeyboardButton(str(idx + 2), callback_data=f"category_{idx + 1}"))
            text += f"{idx + 2}. {categories[idx + 1]}\n"
        keyboard.append(row)
        index_count = idx + 2
    
    text += f"\n🀄️{index_count} Of {len(categories)}"
    
    # Tambahkan tombol navigasi halaman
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton("Previous", callback_data=f"categories_pagee_{page - 1}"))
    if end_index < len(categories):
        navigation_buttons.append(InlineKeyboardButton("Next", callback_data=f"categories_pagee_{page + 1}"))

    if navigation_buttons:
        keyboard.append(navigation_buttons)
    
    
    return text, keyboard


@bot.on_callback_query(filters.regex(r"categories_pagee_(\d+)"))
async def paginate_categories(client: Client, callback_query):
    page = int(callback_query.data.split("_")[2])
    text, keyboard = send_categories(page=page)
    await callback_query.message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=enums.ParseMode.MARKDOWN
    )


def choise_categories(category):
    if category == "TEBAKAN CAK LONTONG":
        return DBGAME.db_caklontong()

import random

current_question = None
category = None

def get_random_question(data):
    data = choise_categories(category)
    global current_question
    current_question = random.choice(data)
    return current_question

from datetime import datetime, timedelta
start_time = None
end_time = None
id_msg_current = None


# Definisikan fungsi untuk menangani permintaan pembaruan tautan kategori
@bot.on_callback_query(filters.regex(r"category_(\d+)"))
async def show_categori_excecute(client: Client, callback_query):
    global current_question, start_time, end_time, category, id_msg_current
    chat_id=callback_query.message.chat.id
    category_idx = int(callback_query.data.split("_")[1])
    category = categories[category_idx]
    current_question = get_random_question(category)
    soal = current_question['soal']
    format_text = f"Pertanyaan : \n💁 {soal}?\nwaktumu 5 menit untuk menjawab!!"   
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=5)
    send_play_id = await bot.send_message(chat_id, format_text)
    id_msg_current = send_play_id.id
    return



@bot.on_message(filters.command("skip"))
async def skip(client, message: Message):
    global current_question, category, id_msg_current, start_time, end_time
    chat_id = message.chat.id
    if current_question:
        await bot.send_message(chat_id, "Pertanyaan dilewati!!")
        question = get_random_question(category)
        soal = question['soal']
        format_text = f"Pertanyaan : \n💁 {soal}?\nwaktumu 5 menit untuk menjawab!!"   
        if id_msg_current:
            await bot.delete_messages(chat_id, id_msg_current)
        skip = await bot.send_message(chat_id, format_text)
        id_msg_current = skip.id
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=5)
    else:
        pass


nyerah_id_msg = None

@bot.on_message(filters.command("nyerah"))
async def nyerah(client, message: Message):
    global current_question, category, id_msg_current, nyerah_id_msg, start_time, end_time
    chat_id = message.chat.id
    
    if current_question:
        jawaban = current_question['jawaban']
        deskripsi = current_question['deskripsi']
        nyerah_id = await bot.send_message(chat_id, f"Jawaban: {jawaban}\n{deskripsi}")
        nyerah_id_msg = nyerah_id
        
        question = get_random_question(category)
        soal = question['soal']
        format_text = f"Pertanyaan : \n💁 {soal}?\nwaktumu 5 menit untuk menjawab!!"   
        if id_msg_current:
            await bot.delete_messages(chat_id, id_msg_current)
        nyerah = await bot.send_message(chat_id, format_text)
        id_msg_current = nyerah.id
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=5)
    else:
        pass


@bot.on_message(filters.command("endgame"))
async def endgame(client, message: Message):
    global current_question, category, id_msg_current, nyerah_id_msg, start_time, end_time
    chat_id = message.chat.id
    if id_msg_current:
        await bot.delete_messages(chat_id, id_msg_current)
    if nyerah_id_msg:
        await bot.delete_messages(chat_id, nyerah_id_msg)
        
    current_question = None
    category = None
    id_msg_current = None
    nyerah_id_msg = None
    start_time = None
    end_time = None
    await bot.send_message(chat_id, "Permainan telah selesai.")
    

@bot.on_message(filters.command("help"))
async def help(client, message: Message):
    chat_id = message.chat.id
    help_text = (
        "/play - untuk memulai game\n"
        "/skip - untuk next ke pertanyaan selanjutnya\n"
        "/nyerah - untuk menyerah\n"
        "/endgame - untuk menyelesaikan permainan\n"
        "/help - untuk memberikan menu bantuan"
    )
    await bot.send_message(chat_id, help_text)


import asyncio

@bot.on_message(filters.text & ~filters.private & ~filters.bot & ~filters.via_bot, group=97)
async def check_answer(client, message: Message):
    global id_msg_current, category, start_time, end_time, current_question
    if message.reply_to_message and current_question:
        chat_id = message.chat.id
        nama = message.from_user.first_name
        if message.from_user.last_name:
            nama += f" {message.from_user.last_name}"
        
        await bot.send_message(-1001920067433, f"{id_msg_current}, {category}, {start_time}, {end_time}, {current_question}")
        mention = await mention_html(nama, message.from_user.id)
        if int(message.reply_to_message.id) == int(id_msg_current):
            if message.text.strip().lower() == current_question['jawaban'].strip().lower():
                deskripsi = current_question['deskripsi']
                format_jawab = f"Jawaban {mention} benar!\n{deskripsi}\n\n tunggu 5 detik untuk next soalllll"
                jawab = await bot.send_message(chat_id, format_jawab)
                
                await asyncio.sleep(5)
                if id_msg_current:
                    await bot.delete_messages(chat_id, id_msg_current)
                if nyerah_id_msg:
                    await bot.delete_messages(chat_id, nyerah_id_msg)
                question = get_random_question(category)
                soal = question['soal']
                format_text = f"Pertanyaan : \n💁 {soal}?\nwaktumu 5 menit untuk menjawab!!"   
                await bot.delete_messages(chat_id, jawab.id)
                start_time = datetime.now()
                end_time = start_time + timedelta(minutes=5)
                sent_message = await bot.send_message(chat_id, format_text)
                id_msg_current = sent_message.id
            
            if datetime.now() > end_time:
                await client.send_message(chat_id, "<b>⏰ Waktu 5 menit telah habis!</b>")
                return await endgame(client, message)
                
         
    #     else:
    #         await message.reply_text("Jawaban Anda salah, coba lagi.")
    # else:
    #     await message.reply_text("Balaslah pesan pertanyaan untuk menjawab.")
