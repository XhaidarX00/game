from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pytgcalls import PyTgCalls

OWNER_ID = [2099942562, 5032883349]

# Ganti nilai api_id dan api_hash dengan nilai milik Anda
api_id = 18207302
api_hash = 'a2526b0eea73aa82080ab181f03e0149'
bot_token = '6226509553:AAF4fnIOtCKoj93ORg0bFgvm4VO1w9rlLjY'

# Buat objek klien Pyrogram
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

ubot = Client(
    'py-tgcalls',
    api_id=18207302,
    api_hash='a2526b0eea73aa82080ab181f03e0149',
)

TARGET = -1001453211087

async def write_to_file(data, filename):
    with open(filename, 'w') as file:
        file.write(data)

async def send_document_bot(client, filename, file):
    data_count = len(file)
    text_data = str(file)
    text_data += f"\n\nTotal {filename} : {data_count}"
    
    await write_to_file(text_data, filename)
    await client.send_document(OWNER_ID, filename)

async def main(chat_id):
    async with app:
        async for member in app.get_chat_members(chat_id):
            print(member)

async def main2(chat_id, text):
    async for message in app.get_chat_history(chat_id):
        print(message)
        text += f"{message}\n"
    
    return text


async def count_hashtag_messages(client, group_id, hashtag):
    count = 0
    # Iterasi melalui pesan dalam grup
    async for message in client.search_messages(group_id, query=hashtag):
        # Cek apakah hashtag ada dalam pesan
        if hashtag in message.text:
            count += 1
            
    return count


@ubot.on_message(filters.command('ch') & filters.user(OWNER_ID))
async def show_categories(client: Client, message: Message):
    chat_id = message.chat.id
    hashtag = message.command[1]
    count = await count_hashtag_messages(client, chat_id, hashtag)
    
    await client.send_message(chat_id, f"{hashtag}\n\n{str(count)}")


@app.on_message(filters.command('gm') & filters.user(OWNER_ID))
async def show_categories(client: Client, message: Message):
    chat_id = message.chat.id
    await client.send_message(chat_id, "Processing...")
    text = "Daftar Pesan \n\n"
    text = await main2(chat_id, text)
    await send_document_bot(client, "get_text_member", text)
    
    # chat_id = message.chat.id
    # await client.search_messages_count(chat_id, query=)

@app.on_message(filters.command('ping') & filters.user(OWNER_ID))
async def show_categories(client: Client, message: Message):
    chat_id = message.chat.id
    me = await client.get_me()
    await client.send_message(chat_id, f"Pong!! {me.first_name}")


list_titel = {}

import re

@app.on_message(filters.command("addt") & filters.user(OWNER_ID))
async def testing(client, message):
    chat_id = message.chat.id
    pesan = message.reply_to_message.text if message.reply_to_message else None
    if not pesan:
        return await app.send_message(chat_id, "<b>Silahkan balas ke pesan / data text!!</b>")
    
    # pesan = convert_font(pesan).upper()
    # pattern = re.compile(r'\d+\. (.+?):')
    line_pattern = r"\d+\.\s+(.+?)\s*\|\s*(.+)"
    matches = re.findall(line_pattern, pesan)

    # Hasil matches akan berupa list of tuples
    for match in matches:
        name, title = match
        list_titel[title.strip()] = name
    
    await app.send_message(chat_id, f"Sukses Menambahkan {list_titel}")

@app.on_message(filters.command("dt"))
async def testing(client, message):
    chat_id = message.chat.id
    name = message.from_user.first_name
    
    if message.from_user.last_name:
        name += f" {message.from_user.last_name}"
    
    if len(list_titel) == 0:
        return await app.send_message(chat_id, f"data list titel kosong") 
    
    for titel in list_titel:
        if titel in name:
            return await app.send_message(chat_id, f"{titel} ada di {name}")
        
        # await app.send_message(chat_id, f"{titel} ngga ada di {name}")
    
    
@ubot.on_message(filters.command("tes") & filters.user(OWNER_ID))
async def testing(client, message):
    chat_id = message.chat.id
    hastag = "#ETN"
    async for message in client.search_messages(chat_id, query=hastag):
        # Cek apakah hashtag ada dalam pesan
        print(message)


import requests


vulgar_words = ["vulgafwords", "vulgarwords", "vulgarwords"]

@app.on_message(filters.command("gen") & filters.user(OWNER_ID))
async def handle_message(client, message):
    # client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    # app.send_chat_action(message.chat.id)
    pesan = message.text.lower().split(" ")
    prompt = " ".join(pesan[1:])
    chat_id = message.chat.id
    
    # return await app.send_message(chat_id, prompt)
    
    prompt = translate_message(prompt)
    
    if any(word in prompt for word in vulgar_words):
        client.send_message(
            chat_id=message.chat.id,
            text="❌ <b>You cannot generate images with vulgar prompts.</b>",
            parse_mode="html"
        )
    else:
        api_url = f"https://aiimage.hellonepdevs.workers.dev/?prompt={prompt}&state=url"

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            # await app.send_message(chat_id, str(data))
            me = await app.get_me()
            await client.send_photo(
                chat_id=message.chat.id,
                photo=data["image_url"],
                caption=f"🎨 <b>Image Generated by {me.first_name}</b>",
                parse_mode=enums.ParseMode.HTML
            )

        except Exception as e:
            await client.send_message(
                chat_id=message.chat.id,
                text=f"❌ <b>Error:</b> <i>{str(e)}</i>",
                parse_mode= enums.ParseMode.HTML
            )


from googletrans import Translator

translator = Translator()

def translate_message(pesan):
    # Menerjemahkan pesan
    translated = translator.translate(pesan, src='id', dest='en')

    return translated.text


import emoji

# Fungsi untuk memeriksa apakah sebuah teks mengandung emoji
def contains_emoji(text):
    return any(emoji.is_emoji(char) for char in text)

# Fungsi untuk memisahkan emoji dari teks
def split_text_and_emoji(text):
    text_part = ''.join([char for char in text if not emoji.is_emoji(char)])
    emoji_part = ''.join([char for char in text if emoji.is_emoji(char)])
    return text_part, emoji_part


@app.on_message(filters.text & ~filters.private & ~filters.bot & ~filters.via_bot, group = 99)
async def handle_anti_gcast(client, message):
    chat_id = message.chat.id
    text = message.text
    
    # if contains_emoji(text):
    #     text_part, emoji_part = split_text_and_emoji(text)
    #     await client.send_message(chat_id, f"Emoji Terdeteksi {emoji_part} dari {text_part}")
    
    # else:
    #     await client.send_message(chat_id, "Emoji Tidak Terdeteksi...")
    try:    
        await client.send_message(chat_id, str(message))
    except:
        print(message)
        
    data = message.reply_to_message.photo.file_id
    if data:
        photo = await client.download_media(data)
        
        await app.send_photo(chat_id, photo, "CREATE BY HAIDAR")









# Daftar kategori hewan
categories = ["DIFAMS", "FERNIG", "ELSTON", "BUBBLE", "DIFAMS1", "DIFAMS2", "DIFAMS3"]

link_text = "LINK"
# URL dasar yang akan diembed
base_url = "https://t.me/c/1453211087/"
# Daftar kode yang akan ditambahkan ke URL dasar (hingga 200 item)
link_ids = [
    263101, 263102, 263103, 263104, 263105, 263106, 263107, 263108, 263109, 263110,
    263111, 263112, 263113, 263114, 263115, 263116, 263117, 263118, 263119, 263120,
    263121, 263122, 263123, 263124, 263125, 263126, 263127, 263128, 263129, 263130,
    263131, 263132, 263133, 263134, 263135, 263136, 263137, 263138, 263139, 263140,
    263141, 263142, 263143, 263144, 263145, 263146, 263147, 263148, 263149, 263150,
    263151, 263152, 263153, 263154, 263155, 263156, 263157, 263158, 263159, 263160,
    263161, 263162, 263163, 263164, 263165, 263166, 263167, 263168, 263169, 263170,
    263171, 263172, 263173, 263174, 263175, 263176, 263177, 263178, 263179, 263180,
    263181, 263182, 263183, 263184, 263185, 263186, 263187, 263188, 263189, 263190,
    263191, 263192, 263193, 263194, 263195, 263196, 263197, 263198, 263199, 263200
]


def capitalize_message(message: str) -> str:
    """
    Mengubah kapitalisasi pesan sehingga setiap kata dimulai dengan huruf kapital diikuti oleh huruf kecil.
    
    Args:
        message (str): Pesan yang akan diubah kapitalisasinya.
    
    Returns:
        str: Pesan dengan kapitalisasi yang diubah.
    """
    return ' '.join(word.capitalize() for word in message.split())


# mencari index didalam sebuah list
def find_index(lst, vlu):
    for index, value in enumerate(lst):
        if value == vlu:
            return index
    
    return None


# Membuat kamus dengan indeks sebagai kunci dan nilai berupa kategori
links_by_category = {index: [] for index, category in enumerate(categories)}
# print(f"{links_by_category}\n\nTotal: {len(links_by_category)}")
for idx, link_id in enumerate(link_ids):
    category = categories[idx % len(categories)] # meriset setiap index mencapai kelipatan yang sama
    index = find_index(categories, category)
    if index is not None:
        links_by_category[index].append(link_id)
        

# Fungsi untuk mengirim pesan dengan tautan tertanam
def send_embedded_links(link_text, base_url, link_ids, page=0, per_page=4):
    embedded_links = []
    message_text = f"Daftar Pesan\n"
    start_index = page * per_page
    end_index = start_index + per_page
    index_count = 0
    if len(link_ids) != 0:
        for idx, link_id in enumerate(link_ids[start_index:end_index], start=start_index + 1):
            url = f"{base_url}{link_id}"
            embedded_links.append(url)
            message_text += f"Pesan ke {idx} : [{link_text}]({url})\n"
            index_count = idx
        message_text += f"\n📨 {index_count} Of {len(link_ids)}"
    else:
        message_text += "KOSONG!!"
    
    keyboard = []
    nav_buttons = []
    if start_index > 0:
        nav_buttons.append(InlineKeyboardButton("Previous", callback_data=f"page_{page-1}"))
    if end_index < len(link_ids):
        nav_buttons.append(InlineKeyboardButton("Next", callback_data=f"page_{page+1}"))
    
    keyboard.append(nav_buttons)
    # Tambahkan tombol "Back to Categories" pada baris baru
    keyboard.append([InlineKeyboardButton("Back to Gcs List", callback_data="back_to_categories")])
    
    return message_text, InlineKeyboardMarkup(keyboard)

# Fungsi untuk mengirim daftar kategori
# def send_categories():
#     keyboard = []
#     idx_count = 0
#     text = "Daftar Gcs DiFams\n"
#     for idx, category in enumerate(categories):
#         idx_count = idx
#         if idx % 2 == 0:
#             row = [InlineKeyboardButton(str(idx), callback_data=f"category_{idx}")]
#         else:
#             row.append(InlineKeyboardButton(str(idx), callback_data=f"category_{idx}"))
#             keyboard.append(row)
#     if len(categories) % 2 != 0:
#         keyboard.append([InlineKeyboardButton(str(idx_count + 1), callback_data=f"category_{len(categories) - 1}")])
    
#     return text, keyboard

# Fungsi untuk mengirim daftar kategori
def send_categories(page=0, per_page=4):
    keyboard = []
    text = "Daftar Gcs DiFams\n"
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


# Definisikan fungsi untuk menangani pesan '/embed' yang dipicu oleh pemilik bot
@app.on_message(filters.command('embed') & filters.user(OWNER_ID))
async def show_categories(client: Client, message: Message):
    message_text, keyboard = send_categories()
    await client.send_message(
        chat_id=message.chat.id,
        text=message_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Definisikan fungsi untuk menangani permintaan pembaruan tautan kategori
@app.on_callback_query(filters.regex(r"category_(\d+)"))
async def show_category_links(client: Client, callback_query):
    category_idx = int(callback_query.data.split("_")[1])
    # category = categories[category_idx]
    link_ids = links_by_category[category_idx]
    message_text, keyboard_markup = send_embedded_links(link_text, base_url, link_ids)
    await callback_query.message.edit_text(
        text=message_text,
        reply_markup=keyboard_markup,
        parse_mode=enums.ParseMode.MARKDOWN
    )


# [
#     [
#         pyrogram.types.InlineKeyboardButton(text='Next', callback_data='page_1')
#     ], 
#     [
#         pyrogram.types.InlineKeyboardButton(text='Back to Categories', callback_data='back_to_categories')
#     ]
# ]
    

# Definisikan fungsi untuk menangani permintaan halaman berikutnya atau sebelumnya
@app.on_callback_query(filters.regex(r"page_(\d+)"))
async def on_callback_query(client: Client, callback_query):
    page = int(callback_query.data.split("_")[1])
    # print(callback_query.message.reply_markup.inline_keyboard[0][0].callback_data.split("_")[1])
    # return 
    category_idx = int(callback_query.message.reply_markup.inline_keyboard[0][0].callback_data.split("_")[1])
    # category = categories[category_idx]
    link_ids = links_by_category[category_idx]
    
    message_text, keyboard_markup = send_embedded_links(link_text, base_url, link_ids, page=page)
    await callback_query.message.edit_text(
        text=message_text,
        reply_markup=keyboard_markup,
        parse_mode=enums.ParseMode.MARKDOWN
    )

# Definisikan fungsi untuk kembali ke daftar kategori
@app.on_callback_query(filters.regex(r"back_to_categories"))
async def back_to_categories(client: Client, callback_query):
    message_text, keyboard = send_categories()
    await callback_query.message.edit_text(
        text=message_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


@app.on_callback_query(filters.regex(r"categories_pagee_(\d+)"))
async def paginate_categories(client: Client, callback_query):
    page = int(callback_query.data.split("_")[2])
    text, keyboard = send_categories(page=page)
    await callback_query.message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=enums.ParseMode.MARKDOWN
    )


# Definisikan fungsi untuk menambahkan kategori baru
@app.on_message(filters.command('addc') & filters.user(OWNER_ID))
async def add_category(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Gunakan: /addc [nama kategori]")
        return
    new_category = " ".join(message.command[1:])
    new_category = capitalize_message(new_category)
    if new_category in categories:
        await message.reply_text("Kategori sudah ada.")
    else:
        categories.append(new_category)
        links_by_category[len(categories) - 1] = []
        # print(links_by_category)
        await message.reply_text(f"Kategori '{new_category}' ditambahkan.")

# Definisikan fungsi untuk menghapus kategori
@app.on_message(filters.command('remc') & filters.user(OWNER_ID))
async def remove_category(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Gunakan: /remc [nama kategori]")
        return
    category_to_remove = " ".join(message.command[1:])
    category_to_remove = capitalize_message(category_to_remove)
    if category_to_remove not in categories:
        await message.reply_text("Kategori tidak ditemukan.")
    else:
        index = find_index(categories, category_to_remove)
        categories.remove(category_to_remove)
        print(index)
        if index is not None:
            del links_by_category[index]
            await message.reply_text(f"Kategori '{category_to_remove}' dihapus.")
        await message.reply_text(f"{index}, {category_to_remove}")

# Definisikan fungsi untuk menambahkan link ke kategori
@app.on_message(filters.command('addl') & filters.user(OWNER_ID))
async def add_link(client: Client, message: Message):
    if len(message.command) < 3:
        await message.reply_text("Gunakan: /addl [nama kategori] [link_id]")
        return
    category = message.command[1]
    link_id = message.command[2]
    if category not in categories:
        await message.reply_text("Kategori tidak ditemukan.")
    else:
        index = find_index(categories, category)
        if index is not None:
            links_by_category[index].append(int(link_id))
            await message.reply_text(f"Link ID '{link_id}' ditambahkan ke kategori '{category}'.")

# Definisikan fungsi untuk menghapus link dari kategori
@app.on_message(filters.command('reml') & filters.user(OWNER_ID))
async def remove_link(client: Client, message: Message):
    if len(message.command) < 3:
        await message.reply_text("Gunakan: /reml [nama kategori] [link_id]")
        return
    category = message.command[1]
    link_id = int(message.command[2])
    if category not in categories:
        await message.reply_text("Kategori tidak ditemukan.")
    elif link_id not in links_by_category[category]:
        await message.reply_text("Link ID tidak ditemukan di kategori tersebut.")
    else:
        index = find_index(categories, category)
        if index is not None:
            links_by_category[index].remove(link_id)
            await message.reply_text(f"Link ID '{link_id}' dihapus dari kategori '{category}'.")


# Definisikan fungsi untuk menampilkan menu bantuan
def send_help_menu():
    """
    Menghasilkan pesan bantuan yang berisi daftar perintah.
    
    Returns:
        str: Pesan bantuan yang diformat.
    """
    help_message = """
Menu Bantuan

/embed - Menampilkan daftar kategori.
/addc [nama kategori] - Menambah kategori baru.
/remc [nama kategori] - Menghapus kategori.
/addl [nama kategori] [link_id] - Menambah link ke kategori.
/reml [nama kategori] [link_id] - Menghapus link dari kategori.
    """
    return help_message

@app.on_message(filters.command('helpp') & filters.user(OWNER_ID))
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
        

@app.on_message(filters.command('send') & filters.user(OWNER_ID))
async def help_menu(client: Client, message: Message):
    chat_id  = f"-100{1920067433}"
    await app.send_message(chat_id, "Masuk")


from pytgcalls.types import Update as up

@app.on_raw_update()
async def on_update(_, update: up, __, chats):
    print(f"{update}\n\n{chats}\n\n{__}")


app.call_py = PyTgCalls(app)

async def write_to_file(data, filename):
    with open(filename, 'w') as file:
        file.write(data)

async def send_document_bot(filename, file):
    data_count = len(file)
    text_data = str(file)
    text_data += f"\n\nTotal {filename} : {data_count}"
    
    await write_to_file(text_data, filename)
    await app.send_document(OWNER_ID, filename)

from pyrogram.raw.types.phone import GroupCall

@app.on_message(filters.command("ttes", "") & filters.user(OWNER_ID))
async def GroupCallInfo(client, message):
    chat_id_ = message.chat.id
    input_call = await client.call_py._app.get_full_chat(chat_id_)
    result = await client.invoke(
                GroupCall(
                    call=input_call,
                    participants=[],
                    participants_next_offset='',
                    chats=[],
                    users=[]
                )
            )
    
    await send_document_bot(OWNER_ID, str(result))
    return


# Jalankan aplikasi
app.run()
