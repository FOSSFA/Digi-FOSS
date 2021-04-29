from pyrogram import Client, filters
from pyrogram.types import Message
import sqlite3


@Client.on_message(filters.command("updatedb"))  # اضافه کردن کاربر ها به دیتابیس
async def update_db(c: Client, m: Message):
    count = await c.get_chat_members_count(m.chat.id)
    # print(count)

    con = sqlite3.connect("database.db")   # وصل شدن به دیتا بیس
    cur = con.cursor()

    data = await c.get_chat_members(m.chat.id)
    # print(data)
    for i in range(count):
        print(data[i]["status"])
        # await m.reply_text("@" + str(data[i]["user"]["username"]))
        # پیدا کردن اطلاعات یوزر ها
        name = data[i]["user"]["first_name"]
        username = data[i]["user"]["username"]
        intid = data[i]["user"]["id"]
        if data[i]["status"] == "creator" or data[i]["status"] == "administrator":
            isadmin = True
        else:
            isadmin = False
        warns = 0
        status = data[i]["status"]
        # اضافه کردن اطلاعات به دیتا بیس
        cur.execute("INSERT OR IGNORE INTO USERS VALUES (?,?,?,?,?,?)", (name, username, intid, isadmin, warns, status))
        con.commit()

    await m.reply_text(str(count) + "users added to data base")
    con.close()


# -- انپین کردن --
@Client.on_message(filters.command("unpin") | filters.regex(r"انپین"))
async def unpin_msg(c, m: Message):
    await m.reply_to_message.unpin()
    await m.reply_text("پیام انپین شد!", reply_to_message_id=m.reply_to_message.message_id)


# -- پین کردن --
@Client.on_message(filters.command("pin") | filters.regex(r"پین"))
async def pin_msg(c, m: Message):
    m_id = m.reply_to_message.message_id
    await m.reply_to_message.pin(True, True)
    await m.reply_text("پیام پین شد!", reply_to_message_id=m_id)
