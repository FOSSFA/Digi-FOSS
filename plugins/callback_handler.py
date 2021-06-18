from pyrogram import Client
from pyrogram.types import CallbackQuery
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions

from plugins.querys import verify_user, get_setting, change_answer, change_comment


@Client.on_callback_query()
async def panel(c: Client, m: CallbackQuery):
    data = m.data.split(',')
    # print(data, m.from_user.id)
    if data[0] == "grp_management" and data[1] == str(m.from_user.id):
        await m.edit_message_text("""
×برای پین کردن پیام ها روی پیام ریپلای کرده و یکی از پیام های زیر را ارسال کنید:
`/pin` 
**پین**
📌

×برای انپین کردن پیام ها روی پیام مورد نظر ریپلای کرده و یکی از پیام های زیر را بفرستید:
`/unpin` 
**انپین**

×برای اخطار روی پیام شخص مورد نظر ریپلای کرده و یکی از پیام های زیر را ارسال کنید:
`/warn` 
**اخطار**

×برای حذف همه اخطار های کاربر روی یکی از پیام های کاربر ریپلای کرده و یکی از پیام های زیر را بفرستید:
`/del_warns` 
**حذف اخطار**

×برای ساکت یا میوت کردن کاربر مورد نظر به مدت ۲۴ ساعت روی پیام او ریپلای کرده و یکی از پیلم های زیر را بفرستید:
`/mute` 
**میوت**

×برای حذف سکوت کاربر مورد نظر بر روی پیام کاربر ریپلای کرده و یکی از پیام های زیر را بفرستید:
`/un_mute` 
**حذف سکوت**

×برای بن کردن کاربر از گروه روی پیام او ریپلای کرده و یکی از پیام های زیر را ارسال کنید:
`/ban` 
**بن**

×برای حذف کاربر از لیست سیاه گروه این پیام را ارسال کنید به جای USERNAME ایدی فرد موردنظر را بزارید:
`/unban @USERNAME`

×برای ارتقا کاربر به ادمین گروه دستور زیر را روی پیام کاربر مورد نظر ریپلای گنید:
`/promote` 
**ارتقا**
        """,
                                  reply_markup=InlineKeyboardMarkup(
                                      [
                                          [
                                              InlineKeyboardButton(
                                                  "اوکی، فهمیدم 👌",
                                                  callback_data=f"return,{m.from_user.id}"

                                              ),
                                              InlineKeyboardButton(
                                                  "بستن پنل",
                                                  callback_data=f"cls_pnl,{m.from_user.id}"
                                              )

                                          ]
                                      ]
                                  )

                                  )

    elif data[0] == "fun" and data[1] == str(m.from_user.id):
        await m.answer("اطلاعات این بخش هنوز کامل نشده 😬")

    elif data[0] == "cls_pnl" and data[1] == str(m.from_user.id):  # close panel
        await m.answer("اوکی فعلا ✌")
        await c.delete_messages(m.message.chat.id, m.message.message_id)

    elif data[0] == "return":  # return to previous panel
        await c.answer_callback_query(m.id, "هنو بلد نیستم برگردم عقب ):", show_alert=True, cache_time=2)

    elif data[0] == 'verify' and data[1] == str(m.from_user.id):
        await m.edit_message_text(f"""سلام [{m.from_user.first_name}](tg://user?id={m.from_user.id}) عزیز\n
به گروه {m.message.chat.title} خوش اومدی.
شما تایید کردید که ربات نیستید.""")
        await c.restrict_chat_member(m.message.chat.id, m.from_user.id,
                                     ChatPermissions(can_pin_messages=True, can_send_media_messages=True,
                                                     can_send_messages=True, can_send_games=True,
                                                     can_send_polls=True,
                                                     can_send_stickers=True, can_send_animations=True,
                                                     can_invite_users=True, can_change_info=True,
                                                     can_use_inline_bots=True, can_add_web_page_previews=True))
        verify_user(str(m.message.chat.id).strip("-"), m.from_user.id)  # set is_verified to True

    elif data[0] == "setting" and data[1] == str(m.from_user.id):  # setting
        comment = ""
        answer = ""
        values = get_setting(str(m.message.chat.id).strip('-'))
        if values[0][0] and values[0][1]:
            comment = "کامنت:✅"
            answer = "پاسخ:✅"
        elif values[0][0] and not values[0][1]:
            comment = "کامنت:✅"
            answer = "پاسخ:❌"
        elif not values[0][0] and not values[0][1]:
            comment = "کامنت:❌"
            answer = "پاسخ:❌"
        elif not values[0][0] and values[0][1]:
            comment = "کامنت:❌"
            answer = "پاسخ:✅"
        await m.edit_message_text(
            "تنظیمات گروه:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            comment,
                            callback_data=f"change_comment,{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            answer,
                            callback_data=f"change_answer,{m.from_user.id}"
                        )

                    ],
                    [
                        InlineKeyboardButton(
                            "بستن پنل",
                            callback_data=f"cls_pnl,{m.from_user.id}"
                        )
                    ]
                ]
            )
        )

    elif data[0] == "change_answer" and data[1] == str(m.from_user.id):
        comment = ""
        answer = ""
        value = get_setting(str(m.message.chat.id).strip('-'))
        if value[0][0]:
            comment = "کامنت:✅"
        else:
            comment = "کامنت:❌"

        if change_answer(str(m.message.chat.id).strip('-')):
            answer = "پاسخ:✅"
        else:
            answer = "پاسخ:❌"

        await m.edit_message_reply_markup(
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            comment,
                            callback_data=f"change_comment,{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            answer,
                            callback_data=f"change_answer,{m.from_user.id}"
                        )

                    ],
                    [
                        InlineKeyboardButton(
                            "بستن پنل",
                            callback_data=f"cls_pnl,{m.from_user.id}"
                        )
                    ]
                ]
            )

        )

    elif data[0] == "change_comment" and data[1] == str(m.from_user.id):
        comment = ""
        answer = ""
        value = get_setting(str(m.message.chat.id).strip('-'))
        if value[0][1]:
            answer = "پاسخ:✅"
        else:
            answer = "پاسخ:❌"

        if change_comment(str(m.message.chat.id).strip('-')):
            comment = "کامنت:✅"
        else:
            comment = "کامنت:❌"

        await m.edit_message_reply_markup(
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            comment,
                            callback_data=f"change_comment,{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            answer,
                            callback_data=f"change_answer,{m.from_user.id}"
                        )

                    ],
                    [
                        InlineKeyboardButton(
                            "بستن پنل",
                            callback_data=f"cls_pnl,{m.from_user.id}"
                        )
                    ]
                ]
            )

        )


    elif data[1] != str(m.from_user.id):  # FUN 😂
        await m.answer("نزن خرابش میکنی 😒😤")
