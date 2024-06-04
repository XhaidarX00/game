from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import Client, filters, enums
from app.src.helpers.parser import mention_html
from app import bot, OWNER_ID, udb, load_data_json

import asyncio
import random
from datetime import datetime, timedelta



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


in_game_chat_id = {}
in_kata_kata_chat_id = {}
jawaban_family100 = {}
in_game_chat_id_jawab = {}

# Daftar kategori Game
categories = [
    "ASAH OTAK",
    "TEKA-TEKI",
    "FAMILY 100",
    "SUSUN KATA",
    "TEBAK GAMBAR",
    "SIAPAKAH AKU?",
    "TEBAK - TEBAKAN",
    "TEBAKAN CAK LONTONG",
]

def choise_categories(category):
    if category == "TEBAKAN CAK LONTONG":
        return load_data_json('caklontong')
    elif category == "ASAH OTAK":
        return load_data_json('asahotak')
    elif category == "FAMILY 100":
        return load_data_json('family100')
    elif category == "SIAPAKAH AKU?":
        return load_data_json('siapakahaku')
    elif category == "TEKA-TEKI":
        return load_data_json('tekateki')
    elif category == "TEBAK - TEBAKAN":
        return load_data_json('tebaktebakan')
    elif category == "TEBAK GAMBAR":
        return load_data_json('tebakgambar')
    elif category == "SUSUN KATA":
        return load_data_json('susunkata')
    else:
        return None

def get_random_question(category):
    data = choise_categories(category)
    
    # datas = []
    # seen = set()
    # for data_ in data:
    #     if data_ not in seen:
    #         seen.add(data_)
    #         datas.append(data_)
    
    current_question = random.choice(data)
    return current_question



# Fungsi untuk mengirim daftar kategori
def send_categories(page=0, per_page=4):
    global categories
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

# Definisikan fungsi untuk menangani permintaan pembaruan tautan kategori
@bot.on_callback_query(filters.regex(r"category_(\d+)"))
async def show_categori_excecute(client: Client, callback_query):
    global in_game_chat_id
    chat_id=callback_query.message.chat.id
    msg_id = callback_query.message.id
    category_idx = int(callback_query.data.split("_")[1])
    category = categories[category_idx]
    await bot.delete_messages(chat_id, msg_id)
    await handler_choice_game(chat_id, category)
    

# Menampilkan List Tagall
@bot.on_message(filters.command("game"))
async def handler_play(client, message):
    global in_game_chat_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.from_user.first_name
    if message.from_user.last_name:
        nama += f" {message.from_user.last_name}"
    
    if chat_id in in_game_chat_id:
        await bot.send_message(chat_id, "Mengkahiri Permainan terakhir digrup ini")
        await endgame(client, message)
        
    message_text, keyboard = send_categories()
    user_mention_display = await mention_html(name, user_id)
    text = f"Hai 👋 {user_mention_display}\n Have funn sama gamenya...\n"
    text += message_text
    await client.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        protect_content=True
    )
    

async def delete_message(chat_id):
    global in_game_chat_id
    if in_game_chat_id_jawab.get(chat_id, None):
        id_msg = in_game_chat_id_jawab[chat_id]['id_msg']
        if id_msg:
            await bot.delete_messages(chat_id, id_msg)
            

async def handler_choice_game(chat_id, category, jawab=None):
    global in_game_chat_id, jawaban_family100, in_game_chat_id_jawab
    format_text = None
    id_msg = None
    soal = None
    if jawab:
        question = in_game_chat_id[chat_id]['question']
        soal = question['soal']
        jawaban = question['jawaban']
        format_text = f"💁 {soal}?\n"
        if category == "TEBAKAN CAK LONTONG":
            deskripsi = question['deskripsi']
            format_text = f"Jawaban: {jawaban}\n\n{deskripsi}\n"
        elif category == "FAMILY 100":
            jawaban_user = jawaban_family100[chat_id]
            jawaban = question['jawaban']
            for index, value in enumerate(jawaban):
                if value in jawaban_user:
                    user_mention = jawaban_user[value]
                    format_text += f"{index + 1}. {value} [+1 {user_mention}]\n"
                else:
                    format_text += f"{index + 1}. \n"
        elif category == "SUSUN KATA":
            clue = question['tipe']
            format_text += f"Clue: {clue}\n\nJawaban: {jawaban}\n"
        else:
            return await handler_choice_game(chat_id, category)
        
        await delete_message(chat_id)           
        send_msg_jawab = await bot.send_message(chat_id, format_text, protect_content=True)
        id_msg_jwb = send_msg_jawab.id
        if category != "FAMILY 100":
            await asyncio.sleep(5)
            await bot.delete_messages(chat_id, id_msg_jwb)
            return await handler_choice_game(chat_id, category)
        else:
            in_game_chat_id[chat_id]['id_msg'] = id_msg_jwb
        
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=2)
        in_game_chat_id[chat_id]['endtime'] = end_time
        
        return
    
    else:
        if len(in_game_chat_id_jawab) != 0 and in_game_chat_id_jawab.get(chat_id, None):
            del in_game_chat_id_jawab[chat_id]
        
        if len(jawaban_family100) != 0 and jawaban_family100.get(chat_id, None):
            del jawaban_family100[chat_id]
            
        question = get_random_question(category)
        if category != "TEBAK GAMBAR":
            soal = question['soal']
        else:
            soal = question['img']
            
        format_text = f"GAME {category}\n\n💁 {soal}?\n"
        if category == "FAMILY 100":
            jawaban = question['jawaban']
            for count in range(len(jawaban)):
                format_text += f"{count + 1}.\n"
        elif category == "SUSUN KATA":
            clue = question['tipe']
            format_text += f"Clue: {clue}\n"
            
        format_text += f"\nwaktumu 2 menit untuk menjawab!!" 
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=3)
        
        if chat_id in in_game_chat_id:
            id_msg = in_game_chat_id[chat_id].get('id_msg', None)
            if id_msg:
                await bot.delete_messages(chat_id, id_msg)

        send_msg = await bot.send_message(chat_id, format_text, protect_content=True)
        id_msg = send_msg.id
        
    end_time_total = start_time + timedelta(minutes=5)
    in_game_chat_id[chat_id] = {
        'soal': soal,
        'category': category,
        'id_msg': id_msg,
        'question': question,
        'endtime': end_time,
        'endtimetotal': end_time_total
    }
   
    return



async def handler_endtotal():
    global in_game_chat_id, in_game_chat_id_jawab
    
    for chat_id, value in in_game_chat_id.items():
        end_time = value.get('endtimetotal')
        if datetime.now() > end_time:
            id_msg = chat_id.get('id_msg', None)
            if id_msg:
                await bot.delete_messages(chat_id, id_msg)
                
            if len(in_game_chat_id_jawab) != 0 and in_game_chat_id_jawab.get(chat_id, None):
                del in_game_chat_id_jawab[chat_id]
                
            await bot.send_message(chat_id, "<b>⏰ Waktu tunggu 5 menit telah habis!\nPermainan dihentikan total!!</b>", protect_content=True)
            del in_game_chat_id[chat_id]
            
            return True
        else:
            return None
    
    

async def handler_delete_inkata(chat_id):
    if chat_id in in_kata_kata_chat_id:
        id_msg = in_kata_kata_chat_id[chat_id].get('id_msg', None)
        if id_msg:
            await bot.delete_messages(chat_id, id_msg)
            
        del in_kata_kata_chat_id[chat_id]
        

@bot.on_message(filters.command("skip"))
async def skip(client, message: Message):
    global in_game_chat_id
    chat_id = message.chat.id
    if chat_id in in_game_chat_id:
        category = in_game_chat_id[chat_id]['category']
        await handler_choice_game(chat_id, category)
    else:
        return await bot.send_message(chat_id, "Permainan Belum Dimulai\nKetik /play untuk memulai!!", protect_content=True)
    

@bot.on_message(filters.command("nyerah"))
async def nyerah(client, message: Message):
    global in_game_chat_id
    chat_id = message.chat.id
    if chat_id in in_game_chat_id:
        category = in_game_chat_id[chat_id]['category']
        if category != "FAMILY 100":
            await handler_choice_game(chat_id, category, jawab=True)
    else:
        return await bot.send_message(chat_id, "Permainan Belum Dimulai\nKetik /play untuk memulai!!", protect_content=True)
    


@bot.on_message(filters.command("endgame"))
async def endgame(client, message: Message):
    global in_game_chat_id, in_kata_kata_chat_id
    chat_id = message.chat.id
    if chat_id in in_game_chat_id:
        id_msg = in_game_chat_id[chat_id].get('id_msg', None)
        if id_msg:
            await bot.delete_messages(chat_id, id_msg)
        
        del in_game_chat_id[chat_id]
        await bot.send_message(chat_id, "Permainan telah selesai.", protect_content=True)
        
        await handler_delete_inkata(chat_id)
    else:
        return await bot.send_message(chat_id, "Permainan Belum Dimulai\nKetik /play untuk memulai!!", protect_content=True)
        
    

@bot.on_message(filters.command("helpp"))
async def help(client, message: Message):
    chat_id = message.chat.id
    help_text = (
        "<b>`◉` Game : </b>\n"
        "  /game - untuk memulai game\n"
        "  /skip - untuk next ke pertanyaan selanjutnya\n"
        "  /nyerah - untuk menyerah\n"
        "  /endgame - untuk menyelesaikan permainan\n"
        "  /helpp - untuk memberikan menu bantuan\n"
        "  /truth - untuk memulai game truth\n"
        "  /dare - untuk memulai game dare\n"
        "  /rendom - untuk memilih random truth atau dare\n"
        
        "\n<b>`◉` Kata - Kata : </b>\n"
        "  /gombal - kata - kata gombal untuk kamu\n"
        "  /motivasi - kata - kata motivasi untuk kamu\n"
        
    )
    await bot.send_message(chat_id, help_text, protect_content=True)


# truth dare random

@bot.on_message(filters.command("truth"))
async def handler_truth(client, message):
    global in_game_chat_id, in_kata_kata_chat_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.from_user.first_name
    if message.from_user.last_name:
        nama += f" {message.from_user.last_name}"
    
    if chat_id in in_game_chat_id:
        await bot.send_message(chat_id, "Mengkahiri Permainan terakhir digrup ini")
        await endgame(client, message)
    
    data = load_data_json('truth')
    question = random.choice(data)
    mention = await mention_html(name, user_id)
    emot = random.choice(emoticons)
    format_text = f"Truth untuk {mention} {emot}\n\n{question}"
    send_msg = await bot.send_message(chat_id, format_text, protect_content=True)
    
    await handler_delete_inkata(chat_id)
    in_kata_kata_chat_id[chat_id] = {
        'id_msg': send_msg.id
    }


@bot.on_message(filters.command("dare"))
async def handler_dare(client, message):
    global in_game_chat_id, in_kata_kata_chat_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.from_user.first_name
    if message.from_user.last_name:
        nama += f" {message.from_user.last_name}"
    
    if chat_id in in_game_chat_id:
        await bot.send_message(chat_id, "Mengkahiri Permainan terakhir digrup ini")
        await endgame(client, message)
    
    data = load_data_json('dare')
    question = random.choice(data)
    mention = await mention_html(name, user_id)
    emot = random.choice(emoticons)
    format_text = f"Dare untuk {mention} {emot}\n\n{question}"
    send_msg = await bot.send_message(chat_id, format_text, protect_content=True)
    
    await handler_delete_inkata(chat_id)
    in_kata_kata_chat_id[chat_id] = {
        'id_msg': send_msg.id
    }


@bot.on_message(filters.command("random"))
async def handler_random_truth_dare(client, message):
    global in_game_chat_id, in_kata_kata_chat_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.from_user.first_name
    if message.from_user.last_name:
        nama += f" {message.from_user.last_name}"
    
    if chat_id in in_game_chat_id:
        await bot.send_message(chat_id, "Mengkahiri Permainan terakhir digrup ini")
        await endgame(client, message)
    
    random_ = random.choice(['truth', 'dare'])
    data = load_data_json(random_)
    question = random.choice(data)
    mention = await mention_html(name, user_id)
    emot = random.choice(emoticons)
    format_text = f"{random_.capitalize()} untuk {mention} {emot}\n\n{question}"
    send_msg = await bot.send_message(chat_id, format_text, protect_content=True)
    
    await handler_delete_inkata(chat_id)
    in_kata_kata_chat_id[chat_id] = {
        'id_msg': send_msg.id
    }




# bucin

@bot.on_message(filters.command("gombal"))
async def handler_gombal(client, message):
    global in_game_chat_id, in_kata_kata_chat_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.from_user.first_name
    if message.from_user.last_name:
        nama += f" {message.from_user.last_name}"
    
    if chat_id in in_game_chat_id:
        await bot.send_message(chat_id, "Mengkahiri Permainan terakhir digrup ini")
        await endgame(client, message)
    
    data = load_data_json('bucin')
    kata_kata = random.choice(data)
    mention = await mention_html(name, user_id)
    emot = random.choice(emoticons)
    format_text = f"Gombal untuk {mention} {emot}\n\n{kata_kata}"
    send_msg = await bot.send_message(chat_id, format_text, protect_content=True)
    
    await handler_delete_inkata(chat_id)
    in_kata_kata_chat_id[chat_id] = {
        'id_msg': send_msg.id
    } 



# motivasi

@bot.on_message(filters.command("motivasi"))
async def handler_motivasi(client, message):
    global in_game_chat_id, in_kata_kata_chat_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.from_user.first_name
    if message.from_user.last_name:
        nama += f" {message.from_user.last_name}"
    
    if chat_id in in_game_chat_id:
        await bot.send_message(chat_id, "Mengkahiri Permainan terakhir digrup ini")
        await endgame(client, message)
    
    data = load_data_json('motivasi')
    kata_kata = random.choice(data)
    mention = await mention_html(name, user_id)
    emot = random.choice(emoticons)
    format_text = f"Motivasi untuk {mention} {emot}\n\n{kata_kata}"
    send_msg = await bot.send_message(chat_id, format_text, protect_content=True)
    
    await handler_delete_inkata(chat_id)
    in_kata_kata_chat_id[chat_id] = {
        'id_msg': send_msg.id
    }
    
                   


# handler untuk excecute game

@bot.on_message(filters.text & ~filters.private & ~filters.bot & ~filters.via_bot, group=97)
async def check_answer(client, message: Message):
    global in_game_chat_id, jawaban_family100
    chat_id = message.chat.id
    
    if chat_id in in_game_chat_id:
        game_data = in_game_chat_id[chat_id]
        end_time = game_data["endtime"]
        if datetime.now() > end_time:
            await client.send_message(chat_id, "<b>⏰ Waktu 3 menit telah habis!</b>", protect_content=True)
            return await handler_choice_game(chat_id, category)
            
        # endtotal ketika tidak ada permainan selama 10 menit
        endtotal = await handler_endtotal()
        if endtotal:
            return
        
    if not (message.reply_to_message and chat_id in in_game_chat_id):
        return
    
    game_data = in_game_chat_id[chat_id]
    end_time = game_data["endtime"]
    question = game_data["question"]
    category = game_data["category"]
    id_msg = game_data["id_msg"]

    if int(message.reply_to_message.id) != int(id_msg):
        return

    nama = message.from_user.first_name
    if message.from_user.last_name:
        nama += f" {message.from_user.last_name}"
    mention = await mention_html(nama, message.from_user.id)
    
    jawab_user = message.text.strip().lower()

    if category != "FAMILY 100":
        if jawab_user == question["jawaban"].strip().lower():
            await delete_message(chat_id)
                    
            format_jawab = f"Jawaban {mention} benar!\n\nMenunggu 5 detik ke soal selanjutnya!!"
            jawab = await bot.send_message(chat_id, format_jawab, protect_content=True)
            await handler_choice_game(chat_id, category, jawab=True)
            return await bot.delete_messages(chat_id, jawab.id)
    else:
        jawaban = question["jawaban"]
        if jawab_user in jawaban:
            if chat_id not in jawaban_family100:
                jawaban_family100[chat_id] = {jawab_user: mention}
                await handler_choice_game(chat_id, category, jawab=True)
                
            list_jawaban = list(jawaban_family100[chat_id].keys())
            if jawab_user not in list_jawaban:
                jawaban_family100[chat_id].update({jawab_user: mention})
                await handler_choice_game(chat_id, category, jawab=True)
            else:
                pass
                
            if len(jawaban) == len(jawaban_family100[chat_id]):
                await asyncio.sleep(2)
                id_msg = in_game_chat_id[chat_id]['id_msg']
                await handler_choice_game(chat_id, category)
            
            return await bot.delete_messages(chat_id, id_msg)