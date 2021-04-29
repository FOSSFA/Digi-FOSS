from pyrogram import Client, filters
from pyrogram.types import Message
import sqlite3


def create(chat_id):
    dbname = str(chat_id) + ".db"
    con = sqlite3.connect("databases/" + dbname)
    cur = con.cursor()
    cur.execute('''CREATE TABLE USERS 
                    (name text, username text, num_id int NOT NULL unique, is_admin blob, warn int, status text, 
                    is_verified blob)''')

    con.commit()
    con.close()


# chat = '-10328989782321'
# create(chat)

@Client.on_message(filters.command('Create') & filters.user(258564057))
async def db_create(c, m: Message):
    id = m.chat.id
    create(id)
    await m.reply_text("data base created!")
