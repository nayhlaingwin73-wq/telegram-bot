import telebot
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
TOKEN = "8642892449:AAEmVrABAatFXe9cvAsFrbMi1VgImr-_53Q"
ADMIN_ID = 8553448978
bot = telebot.TeleBot(TOKEN)

def extract_numbers(text):
    return " ".join(re.findall(r'\d+', text))

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.caption and re.search(r'\d+', message.caption):

        result = extract_numbers(message.caption)

        user = message.from_user
        username = f"@{user.username}" if user.username else user.first_name

        # ✅ Customer ကို reply ပြန် (clean)
        bot.reply_to(
            message,
            "Order အောင်မြင်ပါသည်✅\nAdmin မှ ငွေလွှဲပြေစာအား စစ်ဆေးနေပါသည်⏳"
        )

        # ✅ Admin button (Done format ပြင်ပြီး)
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                "Done✅",
                callback_data=f"done|{message.chat.id}|{message.message_id}"
            )
        )

        # ✅ Admin ကို photo + info ပို့
        bot.send_photo(
            ADMIN_ID,
            message.photo[-1].file_id,
            caption=f"{message.chat.id}|{username}\n\n{result}",
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    data = call.data.split("|")

    if data[0] == "done":
        chat_id = int(data[1])
        msg_id = int(data[2])

        bot.send_message(
            chat_id,
            "ထည့်ပြီးပါပြီဗျ✅",
            reply_to_message_id=msg_id
        )

        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=None
        )

        bot.answer_callback_query(call.id, "Done!")

print("Bot running 🚀")
bot.infinity_polling()
