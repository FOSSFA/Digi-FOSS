from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("spam"))
async def spam(c, m: Message):
    n = m.text.split(' ')
    n = int(n[1])
    if n > 20:
        await m.reply_text("you cant spam more than 20 message")
    else:
        for i in range(n):
            await m.reply_text("SPAM!" + str(i))


@Client.on_message(filters.command("id"))
async def get_id(c, m: Message):
    await m.reply_text(str(m.reply_to_message.message_id))


@Client.on_message(filters.command("chat_id"))
async def get_cid(c, m: Message):
    await m.reply_text(str(m.chat.id))
