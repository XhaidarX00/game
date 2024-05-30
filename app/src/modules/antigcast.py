import re
from pyrogram.enums import ChatMembersFilter as CMF
from pyrogram import filters
from app import bot, OWNER_ID


is_member = []
is_admin = []

badword_word = [
    "asu", "bot", "ubot", "yubot", "ucelbot", "vcs", "seg", "sex", "tmo", "tek",
    "out", "mi", "sfs", "tekmiout", "biyow"
]

def check_message_word(message):
    # Pisahkan pesan menjadi kata-kata
    words = message.lower()
    for bd in badword_word:
        bd = remove_repeated_chars(bd)
        if bd in words:   
            return True
    
    return False

def remove_repeated_chars(text):
    # Gunakan regex untuk menggantikan huruf yang berulang berturut-turut
    return re.sub(r'(.)\1+', r'\1', text)


@bot.on_message(filters.command("bl"))
async def convertascci(client, message):
    bd = None
    chat_id = message.chat.id
    part = message.text.lower().split()
    if len(part) < 2:
        return await bot.send_message(chat_id, "<b>Gunakan Format : </b> /bl kata_blacklist")
    
    if len(part[1:]) > 2:
        for bd in part[1:]:
            if bd not in badword_word:
                bd = remove_repeated_chars(bd)
                badword_word.append(bd)
    else:
        if part[1] not in badword_word:
            bd = remove_repeated_chars(part[1])
            badword_word.append(bd)
    
    bd_word = " ".join(badword_word)
    await bot.send_message(OWNER_ID, bd_word)
    return await message.reply("<b>Berhasil menambahkan kata Blacklist!</b>")


@bot.on_message(filters.command("rbl"))
async def convertascci(client, message):
    bd = None
    chat_id = message.chat.id
    part = message.text.lower().split()
    if len(part) < 2:
        return await bot.send_message(chat_id, "<b>Gunakan Format : </b> /rbl kata_blacklist")
    
    if len(part[1:]) > 2:
        for bd in part[1:]:
            if bd in badword_word:
                bd = remove_repeated_chars(bd)
                badword_word.remove(bd)
    else:
        if part[1] in badword_word:
            bd = remove_repeated_chars(part[1])
            badword_word.append(bd)
    
    bd_word = " ".join(badword_word)
    await bot.send_message(OWNER_ID, bd_word)
    return await message.reply("<b>Berhasil menghapus kata Blacklist!</b>")

from app.src.helpers.parser import mention_html

@bot.on_message(filters.command("hfree"))
async def convertascci(client, message):
    chat_id = message.chat.id
    if not message.reply_to_message:
        return await client.send_message(chat_id, "Gunakan Format : Replay Pesan")
    
    user = message.reply_to_message.from_user
    
    is_admin.append(user.id)
    user_mention = await mention_html(user.first_name, user.id)
    return await message.reply(f"<b>Berhasil membebaskan {user_mention}</b>")



# Satu baris regex yang menggabungkan semua kondisi
delete_message_regex = re.compile(r'[^\x00-\x7F]|(.)\1{2,}|(\b\w+\b\s+){4,}\b\w+\b')

def should_delete_message(text):
    if len(text.split(" ")) >= 4:
        return False
    
    # Ambil kata pertama dari pesan
    first_word = re.match(r'\b\w+\b', text)

    # Jika kata pertama menggunakan font default, jangan hapus pesan
    if first_word and not re.search(r'[^\x00-\x7F]|(.)\1{2,}', first_word.group()):
        return False

    # Periksa semua kondisi dalam satu regex
    if re.search(delete_message_regex, text):
        return True

    return False


@bot.on_message(filters.text & ~filters.private & ~filters.bot & ~filters.via_bot)
async def handle_anti_gcast(client, message):
    chat_id = message.chat.id
    message_text = message.text
    message_id = message.id
    await client.send_message(chat_id, f"ᴘᴇꜱᴀɴ {message_text}")
    
    if message.forward_sender_name:
        message_id = message.id
        return await client.delete_messages(chat_id, message_id)
        
    if message.from_user.id:
        chat_id = message.chat.id
        user_id = message.from_user.id
        name = message.from_user.first_name
        
        mention = await mention_html(name, user_id)

        if len(is_admin) == 0:
            async for member in client.get_chat_members(chat_id, filter=CMF.ADMINISTRATORS):
                is_admin.append(member.user.id)
        
        if user_id not in is_admin and should_delete_message(message_text):
            await client.delete_messages(chat_id, message_id)
            await client.send_message(chat_id, f"ᴘᴇꜱᴀɴ ᴅᴀʀɪ ᴛᴇʟᴀʜ {mention} ᴛᴇʀʜᴀᴘᴜꜱ")
    