import os
from html import escape
from secrets import choice
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.errors import ChatAdminRequired, RPCError
from pyrogram.types import ChatMemberUpdated, Message
from ..testing.foto import merge_images, resize_and_create_circle_mask, photo_image_path
from ..helpers.string import escape_invalid_curly_brackets, ChatType, build_keyboard, parse_button
from ..helpers.parser import escape_markdown, mention_html
from ..helpers.kbhelper import ikb
from ..helpers.cmd_sender import send_cmd
from app import bot, OWNER_ID



@bot.on_message(filters.command("cfile", "") & filters.user(OWNER_ID))
async def cari_file(client, message):
    nama_file = "foto.jpg"
    current_path = os.getcwd()
    file_path = os.path.join(current_path, nama_file)

    if os.path.exists(file_path):
        await bot.send_message(OWNER_ID, f"File {nama_file} ditemukan di lokasi: {file_path}")
    else:
        await bot.send_message(OWNER_ID, f"File {nama_file} tidak ditemukan.")



@bot.on_message(filters.command("cm", "") & filters.user(OWNER_ID))
async def create_foto(client, message):
    chat_id = message.chat.id
    members = "DAFTAR MEMBERS : \n\n"
    count = 1
    # memberss = []
    async for member in client.get_chat_members(chat_id):
        members += f"{count} [ {member.user.id} ] {member.user.first_name} \n"
        if count < 2:
            await bot.send_message(OWNER_ID, member)
            
        count += 1
        # await bot.send_message(OWNER_ID, str(member))
        # break
        
    filename = "members"
    await write_to_file(str(members), filename)
    await bot.send_document(OWNER_ID, filename)
    # await bot.send_message(OWNER_ID, f"TOTAL : {len(members)}")
    
    
@bot.on_message(filters.command("cf", "") & filters.user(OWNER_ID))
async def create_foto(client, message):
    chat_id = message.chat.id
    
    if not message.reply_to_message:
        return await client.send_message(chat_id, "Gunakan Format : Replay Pesan")
    
    data = message.reply_to_message.from_user
    photo = data.photo
    fotobig_file_id = photo.big_file_id
    foto_user = await client.download_media(fotobig_file_id)
    
    name = data.first_name
    un = f"@{data.username}"
    resized_overlay_image = resize_and_create_circle_mask(foto_user)
    foto_edit = merge_images(name, un, resized_overlay_image)
    
    await client.send_photo(OWNER_ID, foto_edit)
    
    
    # try:
        # foto_user = await client.download_media(fotobig_file_id)
        # ubot.send_photo()
        # await client.send_photo(OWNER_ID, foto_user)
    
    os.remove(foto_user)
    os.remove(foto_edit)
    
    # except:
        # await client.send_message(OWNER_ID, f"{fotobig_file_id} tidak bisa dikirim")



async def escape_mentions_using_curly_brackets_wl(
    m: ChatMemberUpdated,
    n: bool,
    text: str,
    parse_words: list,
    joined = None,
) -> str:
    teks = await escape_invalid_curly_brackets(text, parse_words)
    if n:
        user = m.new_chat_member.user if m.new_chat_member else m.from_user
    else:
        user = m.old_chat_member.user if m.old_chat_member else m.from_user
    if teks:
        teks = teks.format(
            joined=escape(joined),
            first=escape(user.first_name),
            last=escape(user.last_name or user.first_name),
            fullname=" ".join(
                [
                    escape(user.first_name),
                    escape(user.last_name),
                ]
                if user.last_name
                else [escape(user.first_name)],
            ),
            username=(
                "@" + (await escape_markdown(escape(user.username)))
                if user.username
                else (await (mention_html(escape(user.first_name), user.id)))
            ),
            mention=await (mention_html(escape(user.first_name), user.id)),
            chatname=escape(m.chat.title)
            if m.chat.type != ChatType.PRIVATE
            else escape(user.first_name),
            id=user.id,
        )
    else:
        teks = ""

    return teks




async def write_to_file(data, filename):
    with open(filename, 'w') as file:
        file.write(data)

def path_foto():
    nama_file = "foto.jpg"
    current_path = os.getcwd()
    file_path = os.path.join(current_path, nama_file)
    
    return file_path

id_chat_before = None

@bot.on_chat_member_updated(filters.group)
async def member_has_joined(client, member: ChatMemberUpdated):
    global id_chat_before, photo_image_path
    
    if (
        member.new_chat_member
        and member.new_chat_member.status not in {CMS.BANNED, CMS.LEFT, CMS.RESTRICTED}
        and not member.old_chat_member
    ):
        pass
    else:
        return
    
    if member.new_chat_member:
        user = member.new_chat_member.user 
        joined = str(member.new_chat_member.joined_date )
        # filename = "member.new_chat_member"
        # await write_to_file(str(member), filename)
        # await bot.send_document(OWNER_ID, filename)
    else:
        user = member.from_user
        # filename = "member.from_user"
        # await write_to_file(str(member), filename)
        # await bot.send_document(OWNER_ID, filename)
    
    # if member.new_chat_member:
    #     await client.send_message(OWNER_ID, member.new_chat_member)
    # else:
    #     await client.send_message(OWNER_ID, member.from_user)
    
    # return await client.send_message(OWNER_ID, user)
    

    try:
        me = await client.get_me()
        if user.id == me.id:
            return
        if user.is_bot:
            return  # ignore bots
    except ChatAdminRequired:
        return
    
    if joined:
        oo = """WELCOME TO {chatname}
╭━━━━━━━━━━━━━━━━━
┞◈ Waktu : {joined}
┞◈ Nama  : {first}
┟◈ ID         : {id}
┟◈ Une      : {username}
╰━━━━━━━━━━━━━━━━━
 ◉ 🄴🄽🄹🄾🅈🅈🅈 🄸🅃 ◉
"""

# Disini Tempat Sharing atau nongkrong santuy sambil cerita, So enjooyy it !!! 
    
    else:
        oo = """WELCOME TO {chatname}
╭━━━━━━━━━━━━━━━━━
┞◈ Nama  : {first}
┟◈ ID         : {id}
┟◈ Une      : {username}
╰━━━━━━━━━━━━━━━━━
 ◉ 🄴🄽🄹🄾🅈🅈🅈 🄸🅃 ◉
"""
    if user.photo:
        foto_user = user.photo.big_file_id
        foto_user = await client.download_media(foto_user)
    else:
        foto_user = path_foto()
        
    name = user.first_name
    if user.last_name:
        name += f" {user.last_name}"
    
    if user.username:
        un = f"@{user.username}"
    else:
        un = "No Username"
        
    resized_overlay_image = await resize_and_create_circle_mask(foto_user)
    foto_edit = await merge_images(name, un, resized_overlay_image)
    UwU = foto_edit
    mtype = 3
    parse_words = [
        "joined",
        "first",
        "last",
        "fullname",
        "username",
        "mention",
        "id",
        "chatname",
    ]
    
    if joined:
        hmm = await escape_mentions_using_curly_brackets_wl(member, True, oo, parse_words, joined)
    else:
        hmm = await escape_mentions_using_curly_brackets_wl(member, True, oo, parse_words)
    
    hmm += "\n[MUSEUM](buttonurl:https://t.me/sinikedifams)"
    tek, button = await parse_button(hmm)
    
    # await bot.send_message(OWNER_ID, f"{tek} {button}")
    
    button = await build_keyboard(button)
    button = ikb(button) if button else None
    
    if "%%%" in tek:
        filter_reply = tek.split("%%%")
        teks = choice(filter_reply)
    else:
        teks = tek
    
    if id_chat_before:
        try:
            await client.delete_messages(member.chat.id, int(id_chat_before))
        except RPCError:
            pass
        
    if not teks:
        teks = "Hallo {first}, welcome to {chatname} Kawannn ..."
    
    # await bot.send_message(OWNER_ID, teks)
    
    try:
        if not UwU:
            jj = await client.send_message(
                member.chat.id,
                text=teks,
                reply_markup=button,
                disable_web_page_preview=True,
            )
        elif UwU:
            jj = await (await send_cmd(client, mtype))(
                member.chat.id,
                UwU,
                caption=teks,
                reply_markup=button,
            )

        if jj:
            id_chat_before = int(jj.id)
            
    except RPCError as e:
        await bot.send_message(OWNER_ID, str(e))
        
        os.remove(foto_user)
        os.remove(foto_edit)
        return
    
    os.remove(foto_user)
    os.remove(foto_edit)