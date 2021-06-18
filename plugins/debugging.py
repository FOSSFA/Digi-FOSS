from time import sleep

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

admin = 258564057


@Client.on_message(filters.command("spam") & filters.user(admin))
async def spam(c, m: Message):
    # print(" ".join(m.command[1:]))
    n = int(m.command[1])
    msg = " ".join(m.command[2:])
    try:
        if n > 20:
            await m.reply_text("you cant spam more than 20 message")
        else:
            for i in range(n):
                await m.reply_text(f"{msg} 💣")
    except FloodWait as e:
        sleep(e.x)


@Client.on_message(filters.command("id") & filters.user(admin))
async def get_id(c, m: Message):
    await m.reply_text(str(m.reply_to_message.message_id))


@Client.on_message(filters.command("chat_id") & filters.user(admin))
async def get_cid(c, m: Message):
    await m.reply_text(str(m.chat.id))


@Client.on_message(filters.command("test"))
async def test(c: Client, m: Message):
    await m.reply_text(f"hello {m.from_user.mention}")
