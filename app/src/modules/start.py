from pyrogram import filters
from app import bot, OWNER_ID

@bot.on_message(filters.command("startgem"))
async def handle_start_command(client, message):
    
    name_tamu = message.from_user.first_name
    
    text = f"""Halo yang {name_tamu}! Saya Darma 🤖, Silahkan klik /help untuk melihat menu bantuan saya..!"""
    
    await client.send_message(message.from_user.id, text)


@bot.on_message(filters.command('ping') & filters.user(OWNER_ID))
async def show_categories(client, message):
    chat_id = message.chat.id
    me = await client.get_me()
    await client.send_message(chat_id, f"Pong!! {me.first_name}")
    

text = """Halo yang {name_tamu}! Saya Darma dan Darmi 🤖, chatbot ramah Anda. Saya dapat menjawab pertanyaan Anda dengan cara percakapan dan bahkan mengenali isi gambar. Mari kita mulai!
    
    /darmi: Mulai ngobrol dengan saya.
    /darma: Sama aja cuma pakai gambar.
    
Jangan ragu untuk menjelajah dan menanyakan apa pun kepada saya!"""