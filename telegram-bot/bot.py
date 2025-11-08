import telebot
from telebot import types

# ТВОЙ ВРЕМЕННЫЙ ТОКЕН
BOT_TOKEN = "8413261067:AAEe_kLk8mQa4T9lv_dfRdi6HeXDa94QHVI"

bot = telebot.TeleBot(BOT_TOKEN)

# Каналы для проверки подписки
CHANNELS = [
    "@dozik_Q",
    "@quot001",
]

# Проверка подписки
def check_subscribe(user_id):
    for channel in CHANNELS:
        try:
            result = bot.get_chat_member(channel, user_id)
            if result.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True


# Команда старт
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if check_subscribe(user_id):
        bot.reply_to(message, "✅ Привет! Доступ открыт. Ты подписан на все каналы!")
    else:
        markup = types.InlineKeyboardMarkup()

        for ch in CHANNELS:
            markup.add(
                types.InlineKeyboardButton(
                    "Подписаться ✅",
                    url=f"https://t.me/{ch[1:]}"
                )
            )

        markup.add(
            types.InlineKeyboardButton(
                "Проверить подписку 🔄",
                callback_data="check"
            )
        )

        bot.send_message(
            message.chat.id,
            "❗ Чтобы получить доступ — подпишись на каналы:",
            reply_markup=markup
        )


# Перепроверка подписки
@bot.callback_query_handler(func=lambda call: call.data == "check")
def recheck(call):
    user_id = call.from_user.id

    if check_subscribe(user_id):
        bot.send_message(call.message.chat.id, "✅ Доступ открыт. Ты подписался!")
    else:
        bot.answer_callback_query(call.id, "❌ Ты ещё не подписался!")


print("✅ БОТ ЗАПУЩЕН НА RENDER 24/7")
bot.infinity_polling()
