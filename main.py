from pyrogram import Client, filters
from pyrogram.types import Message

app = Client(
    "bot",
)

admin = 258564057


@app.on_message(filters.command("start") & filters.user(admin) & filters.group)
async def start(client, message: Message):
    # await message.reply_text("Hello World!", reply_to_message_id=message.message_id)
    await message.reply_text("""
    سلام، ربات با موفقیت نصب شد.
    برای دیدن دستور های ربات /help را بفرستید.
    
    Digi Foss
    """)
    # await message.reply_text("chat: " + str(message.chat))
    # await message.reply_text(str(message.reply_to_message.text))  # اطلاعات درباره پیام رپلای شده
    # await message.reply_text(str(message.photo))
    # await message.reply_to_message.pin(True, True)
    await app.send_message("258564057", "bot started by:@" + str(message.from_user.username))


@app.on_message(filters.command("help"))
async def help_menu(c, m: Message):
    await m.reply_text("""
    حذف پیام ها: /del [number] یا حذف (تعداد پیام)
    اخطار: ریپلای روی کاربر مورد نظر و ارسال پیام : اخطار | /warn
    حذف اخطار: ریپلای روی کاربر و ارسال پبام: حذف اخطار
    اسپم کردن: /spam [number] [text] حداکثر ۲۰ پیام
    
    
    
    """)


app.run()
