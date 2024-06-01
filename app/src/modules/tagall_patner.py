# """
# flow:
# 1. regis user partner
# 2. display list tag all
# 3. if click scrape member chat
# 4. input text
# 5. tagall in 3 minutes
# 6. limit 3 tagall in one day
# """

import asyncio
import ast
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
# from pyrogram.enums import ChatType
from app import bot, OWNER_ID, udb

user_ids_parter = [OWNER_ID]
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

@bot.on_message(filters.command('addutg') & filters.user(OWNER_ID))
async def add_tagall(client: Client, message: Message):
    global user_ids_parter
    if not message.reply_to_message:
        await message.reply_text("<b>Gunakan Format :</b> /addtg Balas ke pesan ")
        return
    new_utg = message.reply_to_message.from_user
    if new_utg.id in user_ids_parter:
        return await message.reply_text(f"{new_utg.first_name} sudah ada dipatner.")
    else:
        user_ids_parter.append(new_utg.id)
        if not udb.exsist("USERTAGALLPATNER"):
            udb.create("USERTAGALLPATNER", str(user_ids_parter))
        else:
            udb.update("USERTAGALLPATNER", str(user_ids_parter))
        await message.reply_text(f"{new_utg.first_name} berhasil ditambahkan.")



@bot.on_message(filters.command('remutg') & filters.user(OWNER_ID))
async def add_tagall(client: Client, message: Message):
    global user_ids_parter
    user_id = None
    name = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        name = message.reply_to_message.from_user.first_name
    else:
        user_id = message.command[1]
        try:
            name = await bot.get_users(user_id)
        except:
            name = await mention_html("SIANU", user_id)
        
    if user_id not in user_ids_parter:
        return await message.reply_text(f"{name} belum ada dipatner.")
    else:
        user_ids_parter.remove(user_id)
        if udb.exsist("GCTAGALLPATNER"):
            udb.update("GCTAGALLPATNER", str(user_ids_parter))
        else:
            await message.reply_text(f"Users Gc Patner Kosong!!")
            
        await message.reply_text(f"{name} berhasil dihapus.")
        

# Menambahkan dan Menghapus Gc Patner

@bot.on_message(filters.command('addtg') & filters.user(OWNER_ID))
async def add_tagall(client: Client, message: Message):
    global list_partner
    chat_id = message.chat.id
    namagc = message.chat.title
    
    new_tg = capitalize_message(namagc)
    if new_tg in list_partner:
        return await message.reply_text("Gc Patner sudah ada.")
    else:
        list_partner[new_tg] = chat_id
        if not udb.exsist("GCTAGALLPATNER"):
            udb.create("GCTAGALLPATNER", str(list_partner))
        else:
            udb.update("GCTAGALLPATNER", str(list_partner))
            
        await message.reply_text(f"Gc Patner '{new_tg}' berhasil ditambahkan.")
    


@bot.on_message(filters.command('deltg') & filters.user(OWNER_ID))
async def add_tagall(client: Client, message: Message):
    global list_partner
    if len(message.command) < 2:
        await message.reply_text("Gunakan: /deltg Nama GC Patner")
        return
    del_tg = " ".join(message.command[1:])
    del_tg = capitalize_message(del_tg)
    if del_tg not in list_partner:
        return await message.reply_text("Gc Patner tidak ditemukan.")
    else:
        del list_partner[del_tg]
        if udb.exsist("GCTAGALLPATNER"):
            udb.update("GCTAGALLPATNER", str(list_partner))
        else:
            await message.reply_text(f"List Gc Patner Kosong!!")
            
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
    """
#         help_message = """
# Menu Bantuan

# /dtg - Menampilkan List GC patner.
# /addtg Nama GC - Menambah GC patner.
# /remtg Nama GC - Menghapus GC patner.
# /addutg Balas Pesan - Menambah user patner bot akses.
# /remutg Balas Pesan - Menghapus user patner bot akses.
#     """
    return help_message

@bot.on_message(filters.command('help'))
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


def remove_duplicate_values(input_dict):
    """
    Menghapus entri dengan nilai duplikat dari dictionary.
    
    Args:
    input_dict (dict): Dictionary asal yang mungkin berisi nilai duplikat.
    
    Returns:
    dict: Dictionary baru dengan nilai-nilai unik.
    """
    unique_values = {}
    seen_values = set()

    for key, value in input_dict.items():
        if value not in seen_values:
            unique_values[key] = value
            seen_values.add(value)

    return unique_values



# Menampilkan List Tagall
@bot.on_message(filters.command('dtg'))
async def show_categories(client: Client, message: Message):
    global list_partner, user_ids_parter
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.from_user.first_name
    if len(list_partner) == 0 or len(user_ids_parter) == 0:
        list_partner_ = udb.read("GCTAGALLPATNER")
        list_partner_ = ast.literal_eval(list_partner_)
        ids_users = udb.read("USERTAGALLPATNER")
        ids_users = ast.literal_eval(ids_users)
        user_ids_parter += ids_users
        if len(list_partner_) == 0:
            return await bot.send_message(chat_id, "List Patner Kosong!!")
        else:
            user_ids_parter += ids_users
            list_partner.update(list_partner_)
            list_partner = remove_duplicate_values(list_partner)
            
    
    message_text, keyboard = send_data_gc_patner()
    user_mention_display = await mention_html(name, user_id)
    text = f"Hai 👋 {user_mention_display}\n"
    text += message_text
    await client.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



# Menampilkan users Tagall
@bot.on_message(filters.command('dutg') & filters.user(OWNER_ID))
async def show_categories(client: Client, message: Message):
    chat_id = message.chat.id
    text = "Daftar Users Tg Patner\n"
    for index, user in enumerate(user_ids_parter, start = 1):
        try:
            user_ = await bot.get_users(user)
            user_mention = user_.mention
            user_id = user_.id
        except:
            user_mention = await mention_html("SIANU", user)
            user_id = user
            
        text += f"{index}. {user_mention} [{user_id}]\n"
    
    await bot.send_message(chat_id, text)
    
    

# Menampilkan List Tagall
@bot.on_message(filters.command('cancel'))
async def show_categories(client: Client, message: Message):
    global on_tagall
    chat_id = message.chat.id
    user_id = message.from_user.id
    is_admin = await check_user_admin(user_id, chat_id)
    if is_admin:
        name_user = message.from_user.first_name
        user_mention_cancel = await mention_html(name_user, user_id)
        on_tagall.remove(chat_id)
        return await bot.send_message(chat_id, f"Tagall dihentikan oleh {user_mention_cancel} !!")


def send_data_gc_patner(page=0, per_page=4):
    global list_partner
    keyboard = []
    text = "Daftar GC Patner Siap tagall\n"
    index_count = 0
    # Tentukan batasan halaman
    start_index = page * per_page
    end_index = min(start_index + per_page, len(list_partner))
    
    keys = list(list_partner.keys())
    values = list(list_partner.values())
    values = [index for index, value in enumerate(values) if value not in on_tagall]
    keys = [keys[index] for index in values]
    
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
from pyrogram.enums import ChatMemberStatus

# Fungsi untuk memeriksa apakah bot memiliki hak admin
async def check_bot_admin(client, chat_id):
    try:
        member = await client.get_chat_member(chat_id, 'me')
        if member.status ==  ChatMemberStatus.ADMINISTRATOR:
            return True
        
    except ChatAdminRequired:
        return False

# Fungsi untuk memeriksa apakah bot memiliki hak admin
async def check_user_admin(user_id, chat_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        if member.status ==  ChatMemberStatus.ADMINISTRATOR:
            return True
        
    except ChatAdminRequired:
        return False


on_tagall = []

# Definisikan fungsi untuk menangani tagall
@bot.on_callback_query(filters.regex(r"listpatner_(\d+)"))
async def handler_tagall_gc(client: Client, callback_query):
    global list_partner, chats_member, on_tagall
    tagall_idx = int(callback_query.data.split("_")[1])
    keys = list(list_partner.keys())
    values = list(list_partner.values())
    namagc = keys[tagall_idx]
    chat_id = values[tagall_idx]
    user_id = callback_query.from_user.id
    msg_tagall = None
    
    # Periksa batas penggunaan
    if int(user_id) != OWNER_ID and not check_usage_limit(user_id):
        return await client.send_message(user_id, "<b>🚫 Kamu telah mencapai batas penggunaan untuk hari ini. Silakan coba lagi besok.</b>")
    
    # Periksa apakah bot memiliki hak admin
    if not await check_bot_admin(client, chat_id):
        return await client.send_message(user_id, f"<b>🚫 Bot belum menjadi admin di grup {namagc}</b>")
    
    try:
        msg = await bot.ask(user_id, "Masukan Kata Tagall\nWaktumu 1 menit", timeout=60)
        msg_tagall = msg.text
    except asyncio.TimeoutError:
        return await client.send_message(user_id, "<b>⏰ Waktu Kamu Habis! Program Berhenti</b>")
    except Exception as e:
        return await bot.send_message(OWNER_ID, f"Error tagall {e}")
    
    members = []
    if len(chats_member) == 0 or chat_id not in chats_member:
        async for member in client.get_chat_members(chat_id):
            members.append(member.user.id)
        chats_member[chat_id] = members
    members = chats_member.get(chat_id)

    await bot.send_message(user_id, f"Memulai Tagall di {namagc} Selama 3 menit")
    
    on_tagall.append(chat_id)
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=2)
    
    msg_tagall_ = f"{msg_tagall}\n"
    count = 0
    for index, member in enumerate(members):
        if datetime.now() > end_time:
            await client.send_message(user_id, "<b>⏰ Waktu 2 menit telah habis! Tagall dihentikan.</b>")
            on_tagall.remove(chat_id)
            return

        user_mention = await mention_html(choice(emoticons), member)
        msg_tagall_ += f"{user_mention} "
        
        if (index + 1) % 10 == 0:
            await client.send_message(chat_id, msg_tagall_)
            await asyncio.sleep(3)
            msg_tagall_ = f"{msg_tagall}\n"  # Reset message after sending

        count = index
        if chat_id not in on_tagall:
            return
            # name_user = callback_query.from_user.first_name
            # user_mention_cancel = await mention_html(name_user, user_id)
            # return await bot.send_message(chat_id, f"Tagall Berhasil oleh {user_mention_cancel}")
    
    if count % 10 == 1:
        await client.send_message(chat_id, msg_tagall_)
    
    return
    
    
    
    
@bot.on_callback_query(filters.regex(r"listpartner_pagee_(\d+)"))
async def paginate_categories(client: Client, callback_query):
    page = int(callback_query.data.split("_")[2])
    text, keyboard = send_data_gc_patner(page=page)
    await callback_query.message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=enums.ParseMode.MARKDOWN
    )