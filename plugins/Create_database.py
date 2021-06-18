import sqlite3
import os
from pyrogram import Client, filters
from pyrogram.types import Message


def create_user(chat_id):
    if not os.path.exists("/app/databases"):
        os.mkdir("/app/databases")
    dbname = str(chat_id) + ".db"
    con = sqlite3.connect("databases/" + dbname)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS USERS 
                    (name text, username text, num_id int NOT NULL unique, is_admin blob, warn int, status text, 
                    is_verified blob)''')

    con.commit()
    con.close()


def create_setting(chat_id):
    dbname = str(chat_id) + ".db"
    con = sqlite3.connect("databases/" + dbname)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS SETTING
                (comment_protector blob, answer_why blob)
    """)
    cur.execute("INSERT INTO SETTING VALUES (?,?)", (True, False))
    con.commit()
    con.close()


# chat = '-10328989782321'
# create(chat)

@Client.on_message(filters.command('Create'))
async def db_create(c, m: Message):
    ids = str(m.chat.id)
    ids = ids.strip('-')
    create_user(ids)
    create_setting(ids)

    await m.reply_text("دیتا بیس ایجاد شد !")
