import telebot
from telebot import types

# ✅ Твой токен
BOT_TOKEN = "8413261067:AAEe_kLk8mQa4T9lv_dfRdi6HeXDa94QHVI"

# ✅ Каналы, на которые нужно подписаться
REQUIRED_CHANNELS = [
    "@dozik_Q",
    "@quot001"
]

# ✅ Канал, к которому даём доступ после подписки
ACCESS_CHANNEL = "https://t.me/the_anxis"

bot = telebot.TeleBot(BOT_TOKEN)


# ✅ Проверка подписки сразу на ВСЕ каналы
def check_all_subs(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.inline_keyboard_markup.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("✅ Проверить подписку", callback_data="check")
    keyboard.add(btn)

    # ✅ Сообщаем пользователю, куда подписываться
    text = "Чтобы получить доступ — подпишись на каналы:\n\n"
    for ch in REQUIRED_CHANNELS:
        text += f"👉 {ch}\n"
    text += "\nПосле подписки нажми кнопку ниже ✅"

    bot.send_message(message.chat.id, text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "check")
def recheck(call):
    user_id = call.from_user.id

    if check_all_subs(user_id):
        bot.send_message(call.message.chat.id, "✅ Ты подписался на все каналы!")
        bot.send_message(
            call.message.chat.id,
            f"🔗 Доступ открыт! Вот ссылка:\n{ACCESS_CHANNEL}"
        )
    else:
        bot.answer_callback_query(call.id, "❌ Ты не подписался на все каналы!")

        text = "Ты должен подписаться на ВСЕ каналы:\n\n"
        for ch in REQUIRED_CHANNELS:
            text += f"👉 {ch}\n"

        bot.send_message(call.message.chat.id, text)


print("✅ Бот запущен!")
bot.infinity_polling()
