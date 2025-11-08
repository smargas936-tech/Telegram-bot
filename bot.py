import telebot
from telebot import types

# ==========================
# ТВОЙ ТЕСТОВЫЙ ТОКЕН
BOT_TOKEN = "8413261067:AAEe_kLk8mQa4T9lv_dfRdi6HeXDa94QHVI"
# ==========================

bot = telebot.TeleBot(BOT_TOKEN)

# Каналы для проверки
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
        except Exception as e:
            print("Ошибка:", e)
            return False
    return True


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if check_subscribe(user_id):
        bot.reply_to(message, "✅ Привет! Ты подписан на все каналы. Добро пожаловать!")
    else:
        markup = types.InlineKeyboardMarkup()
        for ch in CHANNELS:
            btn = types.InlineKeyboardButton(
                "Подписаться ✅",
                url=f"https://t.me/{ch[1:]}"
            )
            markup.add(btn)

        check_btn = types.InlineKeyboardButton(
            "Проверить подписку 🔄",
            callback_data="check"
        )
        markup.add(check_btn)

        bot.send_message(
            message.chat.id,
            "❗ Чтобы пользоваться ботом — подпишись на каналы:",
            reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: call.data == "check")
def recheck(call):
    user_id = call.from_user.id

    if check_subscribe(user_id):
        bot.send_message(call.message.chat.id, "✅ Отлично! Ты подписался!")
    else:
        bot.answer_callback_query(call.id, "❌ Ты ещё не подписался!")


print("✅ БОТ ЗАПУЩЕН")
bot.infinity_polling()
