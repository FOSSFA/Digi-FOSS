from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from pyrogram.errors import exceptions, MessageDeleteForbidden
from time import time
import sqlite3

admin = 258564057


@Client.on_message(filters.command("updatedb") & filters.user(admin) | filters.group)  # اضافه کردن کاربر ها به دیتابیس
async def update_db(c: Client, m: Message):
    count = await c.get_chat_members_count(m.chat.id)
    # print(count)
    dbname = str(m.chat.title) + '.db'

    con = sqlite3.connect("databases/" + dbname)  # وصل شدن به دیتا بیس
    cur = con.cursor()

    data = await c.get_chat_members(m.chat.id)
    # print(data)
    for i in range(count):
        print(data[i]["status"])
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
@Client.on_message(filters.command("unpin") | filters.regex(r"انپین") | filters.group)
async def unpin_msg(c, m: Message):
    await m.reply_to_message.unpin()
    await m.reply_text("پیام انپین شد!", reply_to_message_id=m.reply_to_message.message_id)


# -- پین کردن --
@Client.on_message(filters.command("pin") | filters.regex(r"پین") | filters.regex(r"^📌") | filters.group)
async def pin_msg(c, m: Message):
    m_id = m.reply_to_message.message_id
    await m.reply_to_message.pin(True, True)
    await m.reply_text("پیام پین شد!", reply_to_message_id=m_id)


@Client.on_message(filters.new_chat_members | filters.group)
async def welcome(c, m: Message):
    dbname = str(m.chat.title) + '.db'

    con = sqlite3.connect("databases/" + dbname)  # وصل شدن به دیتا بیس
    cur = con.cursor()

    user = m.from_user
    name = user.first_name
    username = user.username
    ids = user.id
    is_admin = False
    warns = 0
    status = user.status
    is_verified = False

    cur.execute('''INSERT  OR IGNORE INTO USERS VALUES  (?,?,?,?,?,?,?) ''',
                (name, username, ids, is_admin, warns, status, is_verified))
    con.commit()
    con.close()
    await m.reply_text(f"""
    سلام @{m.from_user.username} عزیز
     به گروه {m.chat.title} خوش اومدی‌ ! 

    """)


@Client.on_message(filters.left_chat_member | filters.group)
async def left(c, m: Message):
    dbname = str(m.chat.title) + '.db'
    num_id = int(m.from_user.id)

    con = sqlite3.connect("databases/" + dbname)  # وصل شدن به دیتا بیس
    cur = con.cursor()
    cur.execute("UPDATE USERS SET 'status' = 'left' where num_id=:id", {'id': num_id})
    con.commit()
    # print("Commited!")
    con.close()

    await m.reply_text(f"""
    رفتی ؟ @{m.from_user.username}
    حوالت پا چراغ نفتی 😜
    
    """)


@Client.on_message(
    filters.command("warn") | filters.regex(r"ا+خ+ط+ا+ر") | filters.group)  # TODO check on_Member_updated
async def add_warn(c: Client, m: Message):
    dbname = str(m.chat.title) + '.db'
    num_id = int(m.reply_to_message.from_user.id)
    # print(num_id)
    con = sqlite3.connect("databases/" + dbname)  # وصل شدن به دیتا بیس
    cur = con.cursor()
    cur.execute("SELECT warn FROM USERS where num_id = (?)", (num_id,))
    warns = cur.fetchone()
    cur.execute("UPDATE USERS SET warn =(?) WHERE num_id=(?)", (warns[0] + 1, num_id), )
    con.commit()
    try:
        if warns[0] + 1 < 10:
            await m.reply_text(f"""اخطار داده شد.
            تعداد اخطار های کاربر:@{m.reply_to_message.from_user.username}
            {warns[0] + 1}
            """)
        elif warns[0] + 1 == 10:
            await c.kick_chat_member(m.chat.id, num_id)
            await m.reply_text(f"کاربر @{m.reply_to_message.from_user.id} برای همیشه بن شد.")
            cur.execute("UPDATE USERS SET status =(?) and warn =(?) WHERE num_id =(?)", ('banned', 0, num_id))
    except exceptions.UserAdminInvalid:
        await m.reply_text("چی ؟ چرا باید ادمین رو بن کنم 😐😑")


@Client.on_message(filters.command("del_warns") | filters.regex(r"^ح+ذ+ف+ +ا+خ+ط+ا+ر$") | filters.group)
async def del_warn(c, m: Message):
    dbname = str(m.chat.title) + '.db'
    num_id = int(m.reply_to_message.from_user.id)
    # print(num_id)
    con = sqlite3.connect("databases/" + dbname)  # وصل شدن به دیتا بیس
    cur = con.cursor()
    cur.execute("UPDATE USERS SET warn=(?) where num_id=(?)", (0, num_id,))
    con.commit()
    con.close()
    await m.reply_text(f"اخطار های @{m.reply_to_message.from_user.username} حذف شدند.")


@Client.on_message(filters.command('mute') | filters.regex(r"^م+ی+و+ت") | filters.group)
async def mute(c: Client, m: Message):
    try:
        user_id = m.reply_to_message.from_user.id
    except AttributeError:
        await m.reply_text("کی رو میوت کنم ؟؟ رو کسی ریپلای نکردی 🤔😐")
    chat_id = m.chat.id
    try:
        await c.restrict_chat_member(chat_id, user_id, ChatPermissions(), int(time() + 86400))
        # Client.restrict_chat_member()
        await m.reply_text(f"کاربر @{m.reply_to_message.from_user.username} به مدت ۲۴ ساعت میوت شد😃.")
    except exceptions.UserAdminInvalid:
        await m.reply_text("نمیتونم ادمین هارو میوت کنم اسکل خان 😒")
    except UnboundLocalError:
        pass


@Client.on_message(filters.command("un_mute") | filters.regex(r"ان میوت") | filters.group)
async def un_mute(c: Client, m: Message):
    user_id = m.reply_to_message.from_user.id
    chat_id = m.chat.id
    await c.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=True))
    await m.reply_text(f"@{m.reply_to_message.from_user.username} حالا میتونه حرف بزنه 😒😒😒")


@Client.on_message(filters.command("ban") | filters.regex(r"^ب+ن") | filters.group)
async def ban(c: Client, m: Message):
    dbname = str(m.chat.title) + '.db'
    user_id = m.reply_to_message.from_user.id
    chat_id = m.chat.id

    con = sqlite3.connect("databases/" + dbname)  # وصل شدن به دیتا بیس
    cur = con.cursor()
    cur.execute("UPDATE USERS SET 'status' = 'banned' where num_id=:id", {'id': user_id})
    con.commit()
    await c.kick_chat_member(chat_id, user_id)
    await m.reply_text(f"کاربر به ایدی: @{m.reply_to_message.from_user.username} برای همیشه از گروه بن شد😃")
    con.close()


@Client.on_message(filters.command("unban") | filters.regex(r"^انبن") | filters.group)
async def un_ban(c: Client, m: Message):
    username = m.command[1].strip('@')
    # print(username)
    dbname = str(m.chat.title) + '.db'
    chat_id = m.chat.id
    con = sqlite3.connect('databases/' + dbname)
    cur = con.cursor()
    cur.execute("SELECT num_id FROM USERS WHERE username = (?)", (username,))
    result = cur.fetchone()
    cur.execute("UPDATE USERS SET 'status' = 'member' WHERE num_id =(?)", (result[0],))
    await c.unban_chat_member(chat_id, result[0])
    con.commit()
    await m.reply_text(f"کاربر @{username} حالا میتونه عضو گروه بشه 😒")
    con.close()


# -- حذف پیام --
@Client.on_message(filters.command("del") | filters.regex(r"^حذف") | filters.group)
async def del_10(c, m: Message):
    try:
        counter = 0
        nums = m.text.split(' ')
        nums = int(nums[1])
        msg_id = m.message_id
        while counter != nums:
            if not await c.delete_messages(m.chat.id, msg_id):
                # counter += 1
                msg_id -= 1
            else:
                counter += 1
        await m.reply_text(str(counter) + " پیام پاک شد!")
    except MessageDeleteForbidden:
        await m.reply_text("ربات دسترسی حذف پیام ها را ندارد.")
