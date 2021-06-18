import re
import sqlite3
from time import time as utime

from pyrogram import Client, filters
from pyrogram.errors import exceptions, MessageDeleteForbidden
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatPermissions, ChatMemberUpdated

from plugins.querys import get_admins, get_setting


def m2s(minutes):
    return minutes * 60


def h2s(hour):
    return hour * 3600


@Client.on_message(filters.command("updatedb") & filters.group)  # اضافه کردن کاربر ها به دیتابیس
async def update_db(c: Client, m: Message):
    chat_id = str(m.chat.id).strip('-')
    if get_admins(chat_id, m.from_user.id):
        data = await c.get_chat_members(m.chat.id)
        count = await c.get_chat_members_count(m.chat.id)
        dbname = chat_id + '.db'
        con = sqlite3.connect('databases/' + dbname)
        cur = con.cursor()
        # print(data)
        for i in range(count):
            # print(data[i].status)
            # پیدا کردن اطلاعات یوزر ها
            status = ""
            is_admin = None
            name = data[i].user.first_name
            username = data[i].user.username
            int_id = data[i].user.id
            if data[i].status == "creator" or data[i].status == "administrator":
                is_admin = True
                status = data[i].status
            elif data[i].user.is_bot == 1 or data[i].status != "creator" or data[i].status != "administrator":
                is_admin = False
                status = data[i].status
            warns = 0
            is_verified = True
            # اضافه کردن اطلاعات به دیتا بیس
            cur.execute("INSERT OR IGNORE INTO USERS VALUES (?,?,?,?,?,?,?)",
                        (name, username, int_id, is_admin, warns, status, is_verified))
            con.commit()
        await m.reply_text(str(count) + " کاربر به دیتا بیس اضافه شد.")
        con.close()
    else:
        await m.reply_text("فقط ادمین ها میتونن این کار رو بکنن")


# -- انپین کردن --
@Client.on_message(filters.command("unpin") | filters.regex(r"^ا+ن+پ+ی+ن$") & filters.group)
async def unpin_msg(c, m: Message):
    chat_id = str(m.chat.id).strip('-')
    if get_admins(chat_id, m.from_user.id):
        await m.reply_to_message.unpin()
        await m.reply_text("پیام انپین شد!", reply_to_message_id=m.reply_to_message.message_id)


# -- پین کردن --
@Client.on_message(filters.command("pin") | filters.regex(r"^پ+ی+ن$") | filters.regex(r"^📌") & filters.group)
async def pin_msg(c, m: Message):
    chat_id = str(m.chat.id).strip('-')
    if get_admins(chat_id, m.from_user.id):
        m_id = m.reply_to_message.message_id
        await m.reply_to_message.pin(True, True)
        await m.reply_text("پیام پین شد!", reply_to_message_id=m_id)


@Client.on_message(filters.new_chat_members & filters.group)
async def welcome(c: Client, m: Message):
    print(m.new_chat_members[0]["id"])
    if m.new_chat_members[0]["id"] == 1886243847:
        await m.reply_text("من اووومدم !!!")
    else:
        await c.restrict_chat_member(m.chat.id, m.from_user.id, ChatPermissions())
        dbname = str(m.chat.id).strip('-') + '.db'

        con = sqlite3.connect("databases/" + dbname)  # وصل شدن به دیتا بیس
        cur = con.cursor()
        cur.execute("SELECT num_id FROM USERS WHERE num_id = (?)", (m.from_user.id,))
        users = cur.fetchone()
        if m.from_user.id not in users or users is None :
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
            print("new")
        else:
            cur.execute("UPDATE USERS SET status=(?), is_admin=(?) WHERE main.USERS.num_id = (?)",
                        ("member", False, m.from_user.id))
            print("up")
            con.commit()
        con.close()
        await m.reply_text(
            f"""سلام [{m.from_user.first_name}](tg://user?id={m.from_user.id}) عزیز
    به گروه {m.chat.title} خوش اومدی.
    روی دکمه ی زیر کلیک کن تا بفهمیم ربات نیستی.""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🤖من ربات نیستم🤖",
                            callback_data=f"verify,{m.from_user.id}"
                        )
                    ]
                ]
            )
        )


@Client.on_message(filters.left_chat_member & filters.group)
async def left(c, m: Message):
    dbname = str(m.chat.id).strip('-') + '.db'
    num_id = int(m.from_user.id)

    con = sqlite3.connect("databases/" + dbname)  # وصل شدن به دیتا بیس
    cur = con.cursor()
    cur.execute("UPDATE USERS SET 'status' = 'left', is_admin=0 where num_id=:id", {'id': num_id})
    con.commit()
    # print("Commited!")

    con.close()

    await m.reply_text(f"رفتی [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n حوالت پا چراغ نفتی ")


@Client.on_message(
    filters.command("warn") | filters.regex(r"^ا+خ+ط+ا+ر$") & filters.group)
async def add_warn(c: Client, m: Message):
    # get admins from database
    dbname = str(m.chat.id).strip("-") + '.db'
    if get_admins(str(m.chat.id).strip("-"), m.from_user.id):
        if m.reply_to_message is not None:
            num_id = int(m.reply_to_message.from_user.id)
            con = sqlite3.connect("databases/" + dbname)  # وصل شدن به دیتا بیس
            cur = con.cursor()
            cur.execute("SELECT warn FROM USERS where num_id = (?)", (num_id,))
            warns = cur.fetchone()
            if get_admins(str(m.chat.id).strip("-"), m.reply_to_message.from_user.id):  # check if replied user is admin
                await m.reply_text("من نمیتونم به ادمین های گروه اخطار بدم 😶")
            elif warns[0] + 1 < 10:
                await m.reply_text(f"""
اخطار!
شما{warns[0] + 1} اخطار دریافت کرده اید ، در صورت دریافت 10 اخطار از گروه بن میشوید!
[{m.reply_to_message.from_user.first_name}](tg://user?id={num_id})
""")

                cur.execute("UPDATE USERS SET warn =(?) WHERE num_id=(?)", (warns[0] + 1, num_id), )
                con.commit()  # add warns if user is not admin
                con.close()

            elif warns[0] + 1 == 10:
                await c.kick_chat_member(m.chat.id, num_id)
                await m.reply_text(f"""
[{m.reply_to_message.from_user.first_name}](tg://user?id={num_id})
اخطار به سرت رسیده ، محکوم به بن!
""")
                cur.execute("UPDATE USERS SET status =(?) and warn =(?) WHERE num_id =(?)", ('banned', 0, num_id))
        else:
            await m.reply_text("رو پیامی ریپلای نکردی !")
    else:
        await m.reply_text("نکن بچه 😑😼")


@Client.on_message(
    filters.command("del_warns") | filters.regex(r"^ح+ذ+ف+ +ا+خ+ط+ا+ر$") & filters.group)
async def del_warn(c, m: Message):
    if get_admins(str(m.chat.id).strip("-"), m.from_user.id):
        if m.reply_to_message is not None:
            dbname = str(m.chat.id).strip("-") + '.db'
            num_id = int(m.reply_to_message.from_user.id)
            # print(num_id)
            con = sqlite3.connect("databases/" + dbname)  # وصل شدن به دیتا بیس
            cur = con.cursor()
            cur.execute("SELECT warn FROM USERS where num_id = (?)", (num_id,))  # get warns
            warns = cur.fetchone()

            if warns[0] == 0:
                await m.reply_text(f"[{m.reply_to_message.from_user.first_name}](tg://user?id={num_id})"
                                   f"\nتو هیچ اخطاری نداشتی")
            elif warns[0] == 1:
                await m.reply_text(f"[{m.reply_to_message.from_user.first_name}](tg://user?id={num_id})"
                                   f"\nتو تا الان ۱ اخطار داشتی و چون کاربر خوبی بودی حذف شد؛ افرین!")
                cur.execute("UPDATE USERS SET warn=(?) where num_id=(?)", (warns[0] - 1, num_id,))
                con.commit()
                con.close()
            elif warns[0] > 1:
                await m.reply_to_message.reply_text(
                    f"""[{m.reply_to_message.from_user.first_name}](tg://user?id={num_id})
تو تا الان {warns[0]} تا اخطار داشتی که یکیش کم شد
الان {warns[0] - 1} اخطار داری،‌پس حواست رو جمع کن
""")
                cur.execute("UPDATE USERS SET warn=(?) where num_id=(?)", (warns[0] - 1, num_id,))
                con.commit()
                con.close()
        else:
            await m.reply_text("رو پیام کسی ریپلای نکردی !")


@Client.on_message(filters.command('mute') | filters.regex(r"^م+ی+و+ت") & filters.group)
async def mute(c: Client, m: Message):
    if get_admins(str(m.chat.id).strip("-"), m.from_user.id):
        chat_id = m.chat.id
        user_id = 0
        if m.reply_to_message is not None:
            user_id = m.reply_to_message.from_user.id
        else:
            await m.reply_text("رو پیام کسی ریپلای نکردی. دوباره امتحان بکن")
        try:
            if "ساعت" in m.text:
                index = m.text.find("ساعت")
                index = int(index)
                hour = int(m.text[index - 3:index])
                await c.restrict_chat_member(chat_id, user_id, ChatPermissions(), int(utime() + h2s(hour)))
                await m.reply_to_message.reply_text(
                    f"""[{m.reply_to_message.from_user.first_name}](tg://user?id={user_id})
شما به مدت {hour} ساعت میوت شدید😜
""")
            elif m.command is not None and m.command[2] == "hour":
                hour = m.command[1]
                hour = int(hour)
                await c.restrict_chat_member(chat_id, user_id, ChatPermissions(), int(utime() + h2s(hour)))
                await m.reply_to_message.reply_text(
                    f"""{m.reply_to_message.from_user.mention})
شما به مدت {hour} ساعت میوت شدید😜
""")
            elif "دقیقه" in m.text:
                index = m.text.find("دقیقه")
                minutes = int(m.text[index - 3:index])
                await c.restrict_chat_member(chat_id, user_id, ChatPermissions(), int(utime() + m2s(minutes)))
                await m.reply_to_message.reply_text(
                    f"""[{m.reply_to_message.from_user.first_name}](tg://user?id={user_id})
شما به مدت {minutes} دقیقه میوت شدید😜
                """)
            elif m.command[2] == ("minutes" or "min") and m.command is not None:
                minutes = m.command[1]
                minutes = int(minutes)
                await c.restrict_chat_member(chat_id, user_id, ChatPermissions(), int(utime() + m2s(minutes)))
                await m.reply_to_message.reply_text(f"""
[{m.reply_to_message.from_user.first_name}](tg://user?id={user_id})
شما به مدت {minutes} دقیقه میوت شدید😜
                """)
        except exceptions.UserAdminInvalid:
            await m.reply_text("نمیتونم ادمین هارو میوت کنم :| ")
        # except UnboundLocalError:
        #     pass


@Client.on_message(
    filters.command("unmute") | filters.regex(r"^ا+ن+م+ی+و+ت") | filters.regex(r"^ح+ذ+ف+ +س+ک+و+ت$") & filters.group)
async def un_mute(c: Client, m: Message):
    user_id = m.reply_to_message.from_user.id
    chat_id = m.chat.id
    if get_admins(str(m.chat.id).strip("-"), m.from_user.id):
        await c.restrict_chat_member(chat_id, user_id,
                                     ChatPermissions(can_pin_messages=True, can_send_media_messages=True,
                                                     can_send_messages=True, can_send_games=True, can_send_polls=True,
                                                     can_send_stickers=True, can_send_animations=True,
                                                     can_invite_users=True, can_change_info=True,
                                                     can_use_inline_bots=True, can_add_web_page_previews=True))
        await m.reply_text(f"""
[{m.reply_to_message.from_user.first_name}](tg://user?id={user_id})
حالا میتونی حرف بزنی 😒
""")


@Client.on_message(filters.command("ban") | filters.regex(r"^ب+ن$") & filters.group)
async def ban(c: Client, m: Message):
    if get_admins(str(m.chat.id).strip("-"), m.from_user.id):
        dbname = str(m.chat.id).strip("-") + '.db'
        user_id = m.reply_to_message.from_user.id
        chat_id = m.chat.id

        con = sqlite3.connect("databases/" + dbname)  # وصل شدن به دیتا بیس
        cur = con.cursor()
        cur.execute("UPDATE USERS SET 'status' = 'banned' where num_id=:id", {'id': user_id})
        con.commit()
        await c.kick_chat_member(chat_id, user_id)
        await m.reply_text(f"@{m.reply_to_message.from_user.username} برای همیشه از گروه بن شد😃")
        con.close()


@Client.on_message(filters.command("unban") | filters.regex(r"^ا+ن+ب+ن$") & filters.group)
async def un_ban(c: Client, m: Message):
    if m.reply_to_message is None:
        username = m.command[1].strip('@')
        # print(username)
        dbname = str(m.chat.id).strip('-') + '.db'
        chat_id = m.chat.id
        con = sqlite3.connect('databases/' + dbname)
        cur = con.cursor()
        cur.execute("SELECT num_id FROM USERS WHERE username = (?)", (username,))
        result = cur.fetchone()
        if result is not None:
            cur.execute("UPDATE USERS SET 'status' = 'member' WHERE num_id =(?)", (result[0],))
            await c.unban_chat_member(chat_id, result[0])
            con.commit()
            await m.reply_text(f"@{username} حالا دوباره میتونه عضو گروه بشه 😒")
            con.close()
        else:
            await m.reply_text(
                "همچین کاربری توی گروه نبوده و یا ایدی خودش رو عوض کرده"
                "\nشما میتونید به صورت دستی از تنظیمات گروه کاربر را از بن در بیارید")


# -- حذف پیام --
@Client.on_message(filters.command("del") | filters.regex(r"^حذف$") & filters.group)
async def del_msg(c, m: Message):
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


@Client.on_message(filters.command("promote") | filters.regex(r"^ا+ر+ت+ق+ا$"))
async def set_admin(c: Client, m: Message):
    chat_id = m.chat.id
    user_id = m.reply_to_message.from_user.id
    # print("test1")
    if get_admins(str(chat_id).strip("-"), m.from_user.id):
        if not get_admins(str(chat_id).strip("-"), m.reply_to_message.from_user.id):
            dbname = str(m.chat.id).strip("-") + '.db'
            # user_id = m.reply_to_message.from_user.id
            # chat_id = m.chat.id
            # print("test1")

            con = sqlite3.connect("databases/" + dbname)  # وصل شدن به دیتا بیس
            cur = con.cursor()
            cur.execute("UPDATE USERS SET status = (?) , is_admin=(?)  WHERE num_id = (?)",
                        ('administrator', True, user_id))
            con.commit()
            await c.promote_chat_member(chat_id, user_id, False, True, True, False, False, True, True, True, True)
            await m.reply_text("کاربر ادمین شد (:")
        else:
            await m.reply_text("ایشون که ادمینه \n اسکلمون کردی ؟؟؟")


@Client.on_message(filters.command('^why') | filters.regex(r"^چ+ر+ا.+") | filters.regex(r'^چ+ط+و+ری.+') | filters.regex(
    r"^چ+گ+و+ن+ه.+") | filters.regex(r'^چ+ج+و+ر+ی.+') & filters.group)
async def button(c: Client, m: Message):  # Callback Query handler is in the main.py
    result = get_setting(str(m.chat.id).strip('-'))
    print(result)
    if result[0][1]:
        # txt = m.text.replace('\n', '+').replace(' ', '+')
        txt = m.text
        if "سلام" in txt:
            txt = txt.strip("سلام")

        txt = re.sub(r'\n', ' ', txt)
        txt = re.sub(r'\W+', '+', txt)
        # print(txt)
        url_ddg = f"https://lmddgtfy.ir/?q={txt}"
        url_ggl = f"https://bmbgk.ir/?q={txt}"
        await m.reply_text(
            # m.chat.id,
            "جواب سوالی که پرسیدی به احتمال زیاد اینجاست \n بزن روی یکی از این دکمه ها تاجوابت رو ببنی",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "google",
                            url=url_ggl,
                        ),
                        InlineKeyboardButton(
                            "DuckDuckGo",
                            url=url_ddg,
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            'نمیخوام، اینو ببر',
                            callback_data=f"cls_pnl,{m.from_user.id},{m.chat.id}"
                        )
                    ]

                ]
            )

        )
    else:
        pass


@Client.on_message(filters.command(['s', 'search']))
async def search(c: Client, m: Message):
    txt = ''
    if len(m.command) == 1:
        pass
    else:
        command = m.command[1:]
        for i in range(len(command)):
            txt += command[i] + '+'
        if m.reply_to_message is None:  # check to see if message replied
            url_ddg = f"https://duckduckgo.com/?q={txt}"
            url_ggl = f"https://google.com/search?q={txt}"
            await m.reply_text(
                'جواب سرچ شما در اینترنت:',
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                'داک داک گو',
                                url=url_ddg
                            ),
                            InlineKeyboardButton(
                                'گوگل',
                                url=url_ggl
                            )
                        ],
                    ]
                )

            )
        else:
            url_lmddg = f"https://lmddg.ir/?q={txt}"
            url_bmbgk = f"https://bmbgk.ir/?q={txt}"
            await m.reply_to_message.reply_text(
                'جواب سوال شما با یک سرچ ساده :',
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                'توی داک داک گو',
                                url=url_lmddg
                            ),
                            InlineKeyboardButton(
                                'توی گوگل',
                                url=url_bmbgk
                            )
                        ]
                    ]
                )

            )


@Client.on_message(filters.command("echo") | filters.regex(r'^ا+ک+و'))  # to bot speak instead of you (:
async def echo(c: Client, m: Message):
    if get_admins(str(m.chat.id).strip('-'), m.from_user.id):
        await c.send_chat_action(m.chat.id, "typing")
        if m.command is None and m.reply_to_message is not None:
            await c.delete_messages(m.chat.id, m.message_id)
            await m.reply_to_message.reply_text(
                f'[{"".join(m.text[3:])}](tg://user?id={m.reply_to_message.from_user.id})')

        elif m.command is None and m.reply_to_message is None:
            await c.delete_messages(m.chat.id, m.message_id)
            await m.reply_text(f"{''.join(m.text[3:])}")

        elif m.command is not None and m.reply_to_message is None:
            await c.delete_messages(m.chat.id, m.message_id)
            msg = " ".join(m.command[1:])
            await m.reply_text(msg)

        elif m.reply_to_message is not None and m.command is not None:
            await c.delete_messages(m.chat.id, m.message_id)
            msg = " ".join(m.command[1:])
            await m.reply_to_message.reply_text(f"[{msg}](tg://user?id={m.reply_to_message.from_user.id})")


@Client.on_chat_member_updated(filters.group)
async def updated_user(c: Client, m: ChatMemberUpdated):
    try:
        print(m.new_chat_member.status)
        # ......

        if m.new_chat_member.status == "member":
            chat_id = m.chat.id
            user_id = m.new_chat_member.user.id
            dbname = str(chat_id).strip("-") + '.db'
            con = sqlite3.connect("databases/" + dbname)
            cur = con.cursor()
            cur.execute("UPDATE USERS set is_admin=(?),status=(?) where num_id=(?)",
                        (False, "member", user_id))
            con.commit()
        elif m.new_chat_member.status == "administrator":
            chat_id = m.chat.id
            user_id = m.new_chat_member.user.id
            dbname = str(chat_id).strip("-") + '.db'
            con = sqlite3.connect("databases/" + dbname)
            cur = con.cursor()
            cur.execute("UPDATE USERS SET is_admin=(?),status=(?) WHERE num_id=(?)", (True, "administrator", user_id))
    except AttributeError:
        pass


@Client.on_message(filters.command("leave"))
async def leave(c: Client, m: Message):
    await m.reply_text("بای بای ما رفتیم ):")
    await c.leave_chat(m.chat.id)
