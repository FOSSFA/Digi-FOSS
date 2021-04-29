from pyrogram import Client, filters
from .ramadan import calculate_reminder

CITY = "تهران"

azan_commands = ["ramadan", "azan", "r", 'اذان', 'رمضان', 'مانده', 'افظار', 'گشنمه', 'تشنمه']
azan_messages = ['گشنمه', 'تشنمه']


@Client.on_message(filters.command(azan_commands) | filters.regex('^ت+ش+ن+م+') | filters.regex('^گ+ش+ن+م+'))
def get_reminder(client, message):
    # check if city in list
    command = message['command']

    city = CITY
    if command is None:
        text = message['text']
        if not text is None:
            command = text.split()

    if len(command) == 2:
        city = command[-1]

    rem = calculate_reminder(city)
    text = ':'.join([str(i) for i in rem])
    message.reply(text, quote=True)
