import re
from pyrogram.enums import ChatMembersFilter as CMF
from pyrogram import filters
from app import bot, OWNER_ID, udb
from app.src.modules.tagall_patner import remove_duplicate_values


is_member = []
is_admin = []

# badword_word = [
#     "asu", "bot", "ubot", "yubot", "ucelbot", "vcs", "seg", "sex", "tmo", "tek",
#     "out", "mi", "sfs", "tekmiout", "biyow"
# ]

# def check_message_word(message):
#     # Pisahkan pesan menjadi kata-kata
#     words = message.lower()
#     for bd in badword_word:
#         bd = remove_repeated_chars(bd)
#         if bd in words:   
#             return True
    
#     return False

# def remove_repeated_chars(text):
#     # Gunakan regex untuk menggantikan huruf yang berulang berturut-turut
#     return re.sub(r'(.)\1+', r'\1', text)


# @bot.on_message(filters.command("bl"))
# async def convertascci(client, message):
#     bd = None
#     chat_id = message.chat.id
#     part = message.text.lower().split()
#     if len(part) < 2:
#         return await bot.send_message(chat_id, "<b>Gunakan Format : </b> /bl kata_blacklist")
    
#     if len(part[1:]) > 2:
#         for bd in part[1:]:
#             if bd not in badword_word:
#                 bd = remove_repeated_chars(bd)
#                 badword_word.append(bd)
#     else:
#         if part[1] not in badword_word:
#             bd = remove_repeated_chars(part[1])
#             badword_word.append(bd)
    
#     bd_word = " ".join(badword_word)
#     await bot.send_message(OWNER_ID, bd_word)
#     return await message.reply("<b>Berhasil menambahkan kata Blacklist!</b>")


# @bot.on_message(filters.command("rbl"))
# async def convertascci(client, message):
#     bd = None
#     chat_id = message.chat.id
#     part = message.text.lower().split()
#     if len(part) < 2:
#         return await bot.send_message(chat_id, "<b>Gunakan Format : </b> /rbl kata_blacklist")
    
#     if len(part[1:]) > 2:
#         for bd in part[1:]:
#             if bd in badword_word:
#                 bd = remove_repeated_chars(bd)
#                 badword_word.remove(bd)
#     else:
#         if part[1] in badword_word:
#             bd = remove_repeated_chars(part[1])
#             badword_word.append(bd)
    
#     bd_word = " ".join(badword_word)
#     await bot.send_message(OWNER_ID, bd_word)
#     return await message.reply("<b>Berhasil menghapus kata Blacklist!</b>")

from app.src.helpers.parser import mention_html

@bot.on_message(filters.command("hfree"))
async def convertascci(client, message):
    chat_id = message.chat.id
    if not message.reply_to_message:
        return await client.send_message(chat_id, "Gunakan Format : Replay Pesan")
    
    user = message.reply_to_message.from_user
    
    if user.id in is_admin:
        return await bot.send_message(chat_id, f"{user.first_name}")
    
    is_admin.append(user.id)
    if udb.exsist("HFREE"):
        udb.update("HFREE", str(is_admin))
    else:
        udb.create("HFREE", str(is_admin))
        
    user_mention = await mention_html(user.first_name, user.id)
    return await message.reply(f"<b>Berhasil membebaskan {user_mention}</b>")


@bot.on_message(filters.command("delhfree"))
async def convertascci(client, message):
    chat_id = message.chat.id
    if not message.reply_to_message:
        return await client.send_message(chat_id, "Gunakan Format : Replay Pesan")
    
    user = message.reply_to_message.from_user
    
    if user.id not in is_admin:
        return await bot.send_message(chat_id, f"{user.first_name}")
    
    is_admin.remove(user.id)
    if udb.exsist("HFREE"):
        udb.update("HFREE", str(is_admin))
    else:
        udb.create("HFREE", str(is_admin))
        
    user_mention = await mention_html(user.first_name, user.id)
    return await message.reply(f"<b>Berhasil membatasi {user_mention}</b>")



import emoji

# Fungsi untuk memisahkan emoji dari teks
def split_text_and_emoji(text):
    return ''.join([char for char in text if not emoji.is_emoji(char)])
    # text_part = ''.join([char for char in text if not emoji.is_emoji(char)])
    # emoji_part = ''.join([char for char in text if emoji.is_emoji(char)])
    # return text_part, emoji_part


def should_delete_message(text):
    
    # Filter regex untuk mendeteksi karakter non-ASCII atau simbol khusus
    non_ascii_or_special = re.search(r'[^\x00-\x7F]', text)
    # if non_ascii_or_special:
    #     await bot.send_message(OWNER_ID, "Karakter non-ASCII ")
        
    # Hitung jumlah kata dalam kalimat
    # word_count = len(text.split())
    
    # Filter untuk mendeteksi kode unik atau karakter berulang lebih dari dua kali
    unique_code_pattern = re.search(r'(\W|\d|[A-Za-z])\1{2,}', text)
    # if unique_code_pattern:
    #     await bot.send_message(OWNER_ID, "kode unik atau karakter berulang ")
    
    # Misalnya, kata yang panjangnya antara 8-20 karakter dan memiliki karakter berulang yang tidak wajar
    # random_text_pattern = re.compile(r'^(?=.*[a-zA-Z]{10,20})(?!.*(\w)\1{2,}).*$')
    # random_text_pattern = re.compile(r'^[a-zA-Z]{8,}$')
    # if random_text_pattern.match(text):
    #     await bot.send_message(OWNER_ID, "pesan acak ")
    
    # Jika ada karakter non-ASCII atau simbol khusus, jumlah kata lebih dari 4, ada kode unik, atau pola acak
    # if non_ascii_or_special or word_count > 4 or unique_code_pattern or random_pattern:
    # if non_ascii_or_special or word_count > 4 or unique_code_pattern or random_text_pattern.match(text):
    if non_ascii_or_special or unique_code_pattern:
        return True
    
    return False


import asyncio
import ast

ids_delete_message_notif = []

@bot.on_message(filters.text & ~filters.private & ~filters.bot & ~filters.via_bot, group=99)
async def handle_anti_gcast(client, message):
    global is_admin
    is_admin_ = None
    chat_id = message.chat.id
    message_text = message.text
    message_id = message.id
    
    if message.forward_sender_name:
        return await client.delete_messages(chat_id, message_id)
        
    if message.from_user.id:
        user_id = message.from_user.id
        name = message.from_user.first_name
        
        mention = await mention_html(name, user_id)

        if len(is_admin) == 0:
            async for member in client.get_chat_members(chat_id, filter=CMF.ADMINISTRATORS):
                is_admin.append(member.user.id)
            if udb.exsist("HFREE"):
                is_admin_ = udb.read("HFREE")
                is_admin_ = ast.literal_eval(is_admin_)
                is_admin += is_admin_
                is_admin = remove_duplicate_values(is_admin)
            else:
                pass
        
        text = split_text_and_emoji(message_text)
        if not text:
            return
        
        if user_id not in is_admin and should_delete_message(text):
            await client.delete_messages(chat_id, message_id)
            notif = await client.send_message(chat_id, f"ᴘᴇꜱᴀɴ ᴅᴀʀɪ ᴛᴇʟᴀʜ {mention} ᴛᴇʀʜᴀᴘᴜꜱ")
            ids_delete_message_notif.append(notif.id)
            
    # await client.send_message(chat_id, f"ᴘᴇꜱᴀɴ {message_text} {should_delete_message(message_text)}")


@bot.on_message(filters.text & ~filters.private & ~filters.bot & ~filters.via_bot, group=100)
async def handle_anti_gcast(client, message):
    global ids_delete_message_notif
    chat_id = message.chat.id
    if len(ids_delete_message_notif) != 0:
        for ids_msg in ids_delete_message_notif:
            await client.delete_messages(chat_id, ids_msg)
            await asyncio.sleep(2)
    else:
        pass