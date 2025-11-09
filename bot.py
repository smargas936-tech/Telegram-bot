import telebot
from telebot import types

# ✅ Твой токен (как ты просил, вставляю его полностью)
BOT_TOKEN = "8413261067:AAEe_kLk8mQa4T9lv_dfRdi6HeXDa94QHVI"

# ✅ Канал, на который нужно подписаться
CHANNEL_USERNAME = "@the_anxis"

bot = telebot.TeleBot(BOT_TOKEN)


# ✅ Проверка подписки
def check_subscribe(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False


# ✅ /start
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("✅ Проверить подписку", callback_data="check")
    keyboard.add(btn)

    bot.send_message(
        message.chat.id,
        f"Привет! Чтобы получить доступ — подпишись на канал:\n👉 {CHANNEL_USERNAME}\n\nПосле подписки нажми кнопку ниже.",
        reply_markup=keyboard
    )


# ✅ Кнопка «Проверить подписку»
@bot.callback_query_handler(func=lambda call: call.data == "check")
def recheck(call):
    user_id = call.from_user.id

    if check_subscribe(user_id):
        bot.send_message(call.message.chat.id, "✅ Отлично! Ты подписался!")

        # ✅ Что бот выдаёт после подтверждения
        bot.send_message(
            call.message.chat.id,
            "🔗 Доступ открыт! Вот твоя ссылка:\nhttps://t.me/the_anxis"
        )

    else:
        bot.answer_callback_query(call.id, "❌ Ты ещё не подписался!")
        bot.send_message(
            call.message.chat.id,
            f"❗ Подпишись на канал и попробуй снова:\n👉 {CHANNEL_USERNAME}"
        )


print("✅ Бот запущен!")
bot.infinity_polling()
