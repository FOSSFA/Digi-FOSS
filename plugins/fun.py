from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.querys import get_setting
from plugins.querys import get_admins


@Client.on_message(filters.linked_channel)
async def comment_protector(c: Client, m: Message):
    value = get_setting(str(m.chat.id).strip('-'))
    if value[0][0]:
        # print(m)
        await m.reply_text("کامنت اول !")
        await m.reply_text("کامنت دوم‌ !")
        await m.reply_text("کامنت سوم !")
        # await m.reply_text("کامنت اول تا چهارم توسط این جانب یام یام شد !")
        await m.reply_text("ناموس این پست با موفقیت حفظ شد !")
