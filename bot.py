import telebot
from telebot import types

BOT_TOKEN = "8413261067:AAEe_kLk8mQa4T9lv_dfRdi6HeXDa94QHVI"

CHANNEL_USERNAME = "@the_anxis"

bot = telebot.TeleBot(BOT_TOKEN)

def check_subscribe(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("✅ Проверить подписку", callback_data="check")
    keyboard.add(btn)

    bot.send_message(
        message.chat.id,
        f"Чтобы получить доступ — подпишись на канал:\n👉 {CHANNEL_USERNAME}",
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data == "check")
def recheck(call):
    user_id = call.from_user.id

    if check_subscribe(user_id):
        bot.send_message(call.message.chat.id, "✅ Ты подписан!")

        # ✅ ВСЕГДА присылаем ссылку (без ошибок)
        bot.send_message(
            call.message.chat.id,
            "🔗 Вот твоя ссылка:\nhttps://t.me/the_anxis"
        )

    else:
        bot.answer_callback_query(call.id, "❌ Ты не подписан!")
        bot.send_message(
            call.message.chat.id,
            f"Подпишись на канал:\n👉 {CHANNEL_USERNAME}"
        )


print("✅ Бот запущен!")
bot.infinity_polling()
