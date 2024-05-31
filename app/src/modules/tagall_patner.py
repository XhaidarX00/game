"""
flow:
1. regis user partner
2. display list tag all
3. if click scrape member chat
4. input text
5. tagall in 3 minutes
6. limit 3 tagall in one day
"""

import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
# from pyrogram.enums import ChatType
from app import bot, OWNER_ID

user_ids_parter = []
list_partner = {}

def capitalize_message(message: str) -> str:
    """
    Mengubah kapitalisasi pesan sehingga setiap kata dimulai dengan huruf kapital diikuti oleh huruf kecil.
    
    Args:
        message (str): Pesan yang akan diubah kapitalisasinya.
    
    Returns:
        str: Pesan dengan kapitalisasi yang diubah.
    """
    return ' '.join(word.capitalize() for word in message.split())



# Menambahkan dan Menghapus User Patner

@bot.on_message(filters.command('addutg', "") & filters.user(OWNER_ID))
async def add_tagall(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("<b>Gunakan Format :</b> /addtg Balas ke pesan ")
        return
    new_utg = message.reply_to_message.from_user
    if new_utg in user_ids_parter:
        await message.reply_text(f"{new_utg.first_name} sudah ada dipatner.")
    else:
        user_ids_parter.append(new_utg.id)
        await message.reply_text(f"{new_utg.first_name} berhasil ditambahkan.")


@bot.on_message(filters.command('remutg', "") & filters.user(OWNER_ID))
async def add_tagall(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("<b>Gunakan Format :</b> /remtg Balas ke pesan ")
        return
    del_utg = message.reply_to_message.from_user
    if del_utg not in user_ids_parter:
        await message.reply_text(f"{del_utg.first_name} belum ada dipatner.")
    else:
        user_ids_parter.remove(del_utg.id)
        await message.reply_text(f"{del_utg.first_name} berhasil dihapus.")
        

# Menambahkan dan Menghapus Gc Patner

@bot.on_message(filters.command('addtg', "") & filters.user(OWNER_ID))
async def add_tagall(client: Client, message: Message):
    chat_id = message.chat.id
    namagc = message.chat.title
    new_tg = capitalize_message(namagc)
    if new_tg in list_partner:
        await message.reply_text("Gc Patner sudah ada.")
    else:
        list_partner[new_tg] = chat_id
        await message.reply_text(f"Gc Patner '{new_tg}' berhasil ditambahkan.")


@bot.on_message(filters.command('deltg', "") & filters.user(OWNER_ID))
async def add_tagall(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Gunakan: /deltg Nama GC Patner")
        return
    del_tg = " ".join(message.command[1:])
    del_tg = capitalize_message(del_tg)
    if del_tg not in list_partner:
        await message.reply_text("Gc Patner tidak ditemukan.")
    else:
        del list_partner[del_tg]
        await message.reply_text(f"Gc Patner '{del_tg}' berhasil dihapus.")



# Definisikan fungsi untuk menampilkan menu bantuan

def send_help_menu():
    """
    Menghasilkan pesan bantuan yang berisi daftar perintah.
    
    Returns:
        str: Pesan bantuan yang diformat.
    """
    help_message = """
Menu Bantuan

/dtg - Menampilkan List GC patner.
/addtg Nama GC - Menambah GC patner.
/remtg Nama GC - Menghapus GC patner.
/addutg Balas Pesan - Menambah user patner bot akses.
/remutg Balas Pesan - Menghapus user patner bot akses.
    """
    return help_message

@bot.on_message(filters.command('help') & filters.user(OWNER_ID))
async def help_menu(client: Client, message: Message):
    """
    Mengirimkan menu bantuan ke pengguna saat perintah /help dipanggil.
    
    Args:
        client (Client): Klien bot.
        message (Message): Pesan yang memicu perintah ini.
    """
    try:
        help_text = send_help_menu()
        await message.reply_text(help_text, parse_mode=enums.ParseMode.MARKDOWN)
    except Exception as e:
        # Mengirim pesan error jika terjadi kesalahan
        await message.reply_text(f"Terjadi kesalahan: {e}", parse_mode=enums.ParseMode.MARKDOWN)


# Menampilkan List Tagall
@bot.on_message(filters.command('dtg', "") & filters.user(OWNER_ID))
async def show_categories(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if len(list_partner) == 0:
        return await bot.send_message(chat_id, "List Patner Kosong!!")
    
    message_text, keyboard = send_data_gc_patner()
    await client.send_message(
        chat_id=message.chat.id,
        text=message_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def send_data_gc_patner(page=0, per_page=4):
    keyboard = []
    text = "Daftar List GC Patner\n"
    index_count = 0
    # Tentukan batasan halaman
    start_index = page * per_page
    end_index = min(start_index + per_page, len(list_partner))
    
    keys = list(list_partner.keys())
    
    for idx in range(start_index, end_index, 2):
        text += f"{idx + 1}. {keys[idx]}\n"
        row = [InlineKeyboardButton(str(idx + 1), callback_data=f"listpatner_{idx}")]
        if idx + 1 < end_index:
            row.append(InlineKeyboardButton(str(idx + 2), callback_data=f"listpatner_{idx + 1}"))
            text += f"{idx + 2}. {keys[idx + 1]}\n"
        keyboard.append(row)
        index_count = idx + 2
    
    text += f"\n🀄️{index_count} Of {len(list_partner)}"
    
    # Tambahkan tombol navigasi halaman
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton("Previous", callback_data=f"listpartner_pagee_{page - 1}"))
    if end_index < len(list_partner):
        navigation_buttons.append(InlineKeyboardButton("Next", callback_data=f"listpartner_pagee_{page + 1}"))

    if navigation_buttons:
        keyboard.append(navigation_buttons)
    
    
    return text, keyboard
    

from app.src.helpers.parser import mention_html
from random import choice

chats_member = {}
emoticons = [
    "😈", "👿", "👹", "👺", "🤡", "😺", "🎃", "🤖", "👾", "☠️", "👽", "💀", "👻", "💩",
    "😸", "😹", "😻", "😼", "😽", "😿", "😾", "🖕", "👀", "👶", "👧🏻", "🧒🏻",
    "🧑🏻", "👦🏻", "👩🏻", "👨🏿‍🦰", "👮🏻‍♀️", "🧕🏻", "💂🏻‍♀️", "👷🏻", "👷🏻‍♂️",
    "👩🏻‍🌾", "🧑🏻", "👨🏻‍🌾", "👨🏻‍🍳", "👩🏻‍🎓", "👨🏻‍🎓", "👩🏻‍🚀", "🧑🏻‍🚀",
    "👨🏻‍🎨",  "🤴🏻", "🧞‍♂️", "🧞", "🧞‍♀️", "🧚🏻‍♀️", "🧜🏻‍♂️",
    "🧜🏻", "🧜🏻‍♀️", "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐻‍❄️", "🙈",
    "🐵", "🐸", "🐷", "🦁", "🐮", "🐯", "🐨", "🐒", "🐔", "🐧", "🐦", "🐤", "🐣", "🐥",
    "🐴", "🐗", "🐺", "🦇", "🦉", "🦅", "🐦‍", "🦆", "🦄", "🐝",
    "🐛", "🦋", "🐌", "🐞", "🐜", "🐢", "🦂", "🕷", "🦗", "🦟", "🐍",
    "🦎", "🦖", "🦕", "🐙", "🦑", "🦐", "🦞", "🦈", "🐋", "🐳", "🐬", "🐟",
    "🐠", "🐡", "🦀", "🐊", "🐅", "🐆", "🦓", "🦍", "🦧", "🐘", "🦛", "🐄", "🐂", "🐃",
    "🦘", "🦒", "🐫", "🦏", "🐏", "🦌", "🐕‍🦺", "🐩", "🦜", "🦚", "🦢",
    "🦩", "🕊", "🐇", "🦝", "🦨", "🦔", "🐿", "🐁", "🦥", "🐉", "🐲", "🍄", "🌹",
    "🥀", "🌚", "🌕", "🌖", "🌗", "🌘", "🌑", "🌔", "🌓", "🌒", "🌙", "🌞",
    "🌺", "🌸", "🌼", "⛄️", "🐊", "👑" , "👽", "🎃", "👹", "👺", "🤡", "🎓"
]


from datetime import datetime, timedelta

user_usage = {}

# Fungsi untuk memeriksa dan memperbarui batas penggunaan
def check_usage_limit(user_id):
    now = datetime.now()
    if user_id not in user_usage:
        user_usage[user_id] = []

    # Hapus entri yang lebih lama dari 24 jam
    user_usage[user_id] = [time for time in user_usage[user_id] if now - time < timedelta(hours=24)]

    # Periksa apakah user telah mencapai batas penggunaan
    if len(user_usage[user_id]) >= 3:
        return False

    # Tambahkan waktu penggunaan terbaru
    user_usage[user_id].append(now)
    return True

from pyrogram.errors import ChatAdminRequired

# Fungsi untuk memeriksa apakah bot memiliki hak admin
async def check_bot_admin(client, chat_id):
    try:
        member = await client.get_chat_member(chat_id, 'me')
        return member.status in ['administrator', 'creator']
    except ChatAdminRequired:
        return False

# Definisikan fungsi untuk menangani tagall
@bot.on_callback_query(filters.regex(r"listpatner_(\d+)"))
async def handler_tagall_gc(client: Client, callback_query):
    tagall_idx = int(callback_query.data.split("_")[1])
    keys = list(list_partner.keys())
    values = list(list_partner.values())
    namagc = keys[tagall_idx]
    chat_id = values[tagall_idx]
    user_id = callback_query.from_user.id
    msg_tagall = None
    
    # Periksa batas penggunaan
    if not check_usage_limit(user_id):
        return await client.send_message(user_id, "<b>🚫 Kamu telah mencapai batas penggunaan untuk hari ini. Silakan coba lagi besok.</b>")
    
    # Periksa apakah bot memiliki hak admin
    if not await check_bot_admin(client, chat_id):
        return await client.send_message(user_id, "<b>🚫 Bot belum menjadi admin di grup tersebut. Silakan tambahkan bot sebagai admin.</b>")

    try:
        msg = await client.ask(user_id, "Masukan Kata Tagall\nWaktumu 1 menit", timeout=60)
        msg_tagall = msg.text
    except asyncio.TimeoutError:
        return await client.send_message(user_id, "<b>⏰ Waktu Kamu Habis! Program Berhenti</b>")
    except:
        pass

    members = []
    if len(chats_member) == 0 or chat_id not in chats_member:
        async for member in client.get_chat_members(chat_id):
            members.append(member.user.id)
        chats_member[chat_id] = members

    members = chats_member.get(chat_id)
    
    proses = await bot.send_message(user_id, f"Memulai Tagall di {namagc} Selama 3 menit")
    
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=3)
    
    msg_tagall_ = f"{msg_tagall}\n"
    count = 0
    for index, member in enumerate(members):
        if datetime.now() > end_time:
            await client.send_message(user_id, "<b>⏰ Waktu 3 menit telah habis! Tagall dihentikan.</b>")
            return

        user_mention = await mention_html(emoticons[index % len(emoticons)], member)
        msg_tagall_ += f"{user_mention} "
        
        if (index + 1) % 10 == 0:
            await client.send_message(chat_id, msg_tagall)
            await asyncio.sleep(1)
            msg_tagall_ = f"{msg_tagall}\n"  # Reset message after sending

        count = index
    
    if count % 10 == 1:
        await client.send_message(chat_id, msg_tagall)
    
    await proses.edit_text("Tagall Selesai!!")


    
@bot.on_callback_query(filters.regex(r"listpartner_pagee_(\d+)"))
async def paginate_categories(client: Client, callback_query):
    page = int(callback_query.data.split("_")[2])
    text, keyboard = send_data_gc_patner(page=page)
    await callback_query.message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=enums.ParseMode.MARKDOWN
    )