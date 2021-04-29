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
    await app.send_message("258564057", "bot started by:@" + str(message.reply_to_message.from_user.username))


# -- حذف پیام --
@app.on_message(filters.command("del") | filters.regex(r"حذف"))
async def del_10(c, m: Message):
    counter = 0
    nums = m.text.split(' ')
    nums = int(nums[1])
    msg_id = m.message_id
    while counter != nums:
        if not await app.delete_messages(m.chat.id, msg_id):
            # counter += 1
            msg_id -= 1
        else:
            counter += 1
    await m.reply_text(str(counter) + " پیام پاک شد!")


app.run()
