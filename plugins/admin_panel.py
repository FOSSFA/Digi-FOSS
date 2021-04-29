from pyrogram import Client, filters
from pyrogram.types import Message
import sqlite3

admin = 258564057


@Client.on_message(filters.command("updatedb") & filters.user(admin))  # اضافه کردن کاربر ها به دیتابیس
async def update_db(c: Client, m: Message):
    count = await c.get_chat_members_count(m.chat.id)
    # print(count)
    dbname = str(m.chat.id) + '.db'

    con = sqlite3.connect("databases/" + dbname)  # وصل شدن به دیتا بیس
    cur = con.cursor()

    data = await c.get_chat_members(m.chat.id)
    # print(data)
    for i in range(count):
        print(data[i]["status"])
        # await m.reply_text("@" + str(data[i]["user"]["username"]))
        # پیدا کردن اطلاعات یوزر ها
        name = data[i]["user"]["first_name"]
        username = data[i]["user"]["username"]
        int_id = data[i]["user"]["id"]
        if data[i]["status"] == "creator" or data[i]["status"] == "administrator":
            is_admin = True
        else:
            is_admin = False
        warns = 0
        is_verified = True
        status = data[i]["status"]
        # اضافه کردن اطلاعات به دیتا بیس
        cur.execute("INSERT OR IGNORE INTO USERS VALUES (?,?,?,?,?,?,?)",
                    (name, username, int_id, is_admin, warns, status, is_verified))
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


@Client.on_message(
    filters.new_chat_members | filters.command('wel'))  # TODO چک کن این درست کار میکنه اگه کار کرد یوزر جدید رو به دیتا بیس اضافه کن
async def welcome(c, m: Message):
    await m.reply_text(f"""
    سلام @{m.from_user.username} عزیز
     به گروه {m.chat.title} خوش اومدی‌ ! 
    
    """)
