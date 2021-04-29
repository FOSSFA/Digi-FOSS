from pyrogram import Client, filters
from .ramadan import calculate_reminder

# app = Client("my_account")

CITY = "تهران"

azan_commands = ["ramadan", "azan", "r", 'اذان', 'رمضان', 'مانده', 'افظار', 'گشنمه', 'تشنمه']
azan_messages = ['گشنمه', 'تشنمه']


@Client.on_message(filters.command(azan_commands) | filters.regex('ت+ش+ن+م+') | filters.regex('گ+ش+ن+م+'))
def get_reminder(client, message):
    print("گشنمه")
    # check if city in list
    city = get_city_from_message(message)

    rem = calculate_reminder(city)
    if rem[0] is None:
        message.reply("Service is down.", quote=True)
    else:
        text = ':'.join([str(i) for i in rem])
        message.reply(text, quote=True)


# یه نفر بتونه بگه تایم اذون به من تو هیمن گروه پیام بده ، یا صوت اذون بزار
@Client.on_message(filters.regex('گ+ش+ن+ت+ه+') | filters.regex('ت+ش+ن+ت+ه+'))
def set_azan_reminder(client, message):
    print("گشنمه2")
    # check if city in list
    city = get_city_from_message(message)

    rem = calculate_reminder(city)
    text = ':'.join([str(i) for i in rem])
    message.reply(text, quote=True)


def get_city_from_message(message):
    command = message['command']

    city = CITY
    if command is None:
        text = message['text']
        if not text is None:
            command = text.split(" ", maxsplit=1)

    if len(command) == 2:
        city = command[-1]

    return city

# app.run()
