import telebot
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
TOKEN = "8642892449:AAEmVrABAatFXe9cvAsFrbMi1VgImr-_53Q"
ADMIN_ID = 8553448978
bot = telebot.TeleBot(TOKEN)

def extract_numbers(text):
    return " ".join(re.findall(r'\d+', text))

# user message id store လုပ်ဖို့ dict
user_messages = {}

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.caption and re.search(r'\d+', message.caption):

        result = extract_numbers(message.caption)

        user = message.from_user
        username = f"@{user.username}" if user.username else user.first_name

        # ✅ Customer ကို reply
        sent = bot.reply_to(
            message,
            "Order အောင်မြင်ပါသည်✅\nAdmin မှ ငွေလွှဲပြေစာအား စစ်ဆေးနေပါသည်⏳"
        )

        # ✅ message_id save
        user_messages[message.chat.id] = sent.message_id

        # ✅ Admin button
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                "Done✅",
                callback_data=f"done|{message.chat.id}"
            )
        )

        # ❌ chat id မပြတော့ဘူး
        bot.send_photo(
            ADMIN_ID,
            message.photo[-1].file_id,
            caption=f"{username}\n\n{result}",
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    data = call.data.split("|")

    if data[0] == "done":
        chat_id = int(data[1])

        try:
            # ✅ 1. Customer "Order..." message delete
            if chat_id in user_messages:
                bot.delete_message(chat_id, user_messages[chat_id])

            # ✅ 2. Customer ကို final reply
            bot.send_message(
                chat_id,
                "ထည့်ပြီးပါပြီဗျ✅\nဝယ်ယူအားပေးမှုအတွက်အထူးကျေးဇူးတင်ရှိပါသည်😻"
            )

        except Exception as e:
            print(e)

        try:
            # ✅ 3. Admin photo delete
            bot.delete_message(
                call.message.chat.id,
                call.message.message_id
            )
        except Exception as e:
            print(e)

        bot.answer_callback_query(call.id, "Done!")

print("Bot running 🚀")
bot.infinity_polling()
