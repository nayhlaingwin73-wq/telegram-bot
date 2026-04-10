import telebot
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8642892449:AAEmVrABAatFXe9cvAsFrbMi1VgImr-_53Q"
ADMIN_ID = 8553448978

bot = telebot.TeleBot(TOKEN)

def extract_numbers(text):
    return " ".join(re.findall(r'\d+', text))

user_messages = {}

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.caption and re.search(r'\d+', message.caption):

        result = extract_numbers(message.caption)

        user = message.from_user
        username = f"@{user.username}" if user.username else user.first_name

        # ✅ reply message (bot message only)
        sent = bot.reply_to(
            message,
            "Order confirmed ✅
Checking payment…!Please wait ⏳"
        )

        # ✅ save BOTH ids
        user_messages[message.chat.id] = {
            "order_msg": sent.message_id,
            "user_msg": message.message_id
        }

        # ✅ admin button
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                "Done✅",
                callback_data=f"done|{message.chat.id}"
            )
        )

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
            data_store = user_messages.get(chat_id)

            if data_store:
                # ✅ delete ONLY bot reply (customer side)
                bot.delete_message(chat_id, data_store["order_msg"])

                # ✅ send confirm message
                bot.send_message(
                    chat_id,
                    "ထည့်ပြီးပါပြီဗျ✅\nဝယ်ယူအားပေးမှုအတွက်အထူးကျေးဇူးတင်ရှိပါသည်😻",
                    reply_to_message_id=data_store["user_msg"]
                )

        except Exception as e:
            print(e)

        try:
            # 🔥 REMOVE BUTTON ONLY (message မဖျက်)
            bot.edit_message_reply_markup(
                call.message.chat.id,
                call.message.message_id,
                reply_markup=None
            )
        except Exception as e:
            print(e)

        bot.answer_callback_query(call.id, "Done!")

        
print("Bot running 🚀")
bot.infinity_polling()
