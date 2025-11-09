import telebot
from telebot import types

# ВСТАВЬ СВОЙ ТОКЕН
BOT_TOKEN = "8413261067:AAEe_kLk8mQa4T9lv_dfRdi6HeXDa94QHVI"

bot = telebot.TeleBot(BOT_TOKEN)

# Список каналов для обязательной подписки
CHANNELS = [
    "@dozik_Q",
    "@quot001"
]

# Ссылка после подписки
ACCESS_LINK = "https://t.me/the_anxis"


# Проверка подписки
def check_subscription(user_id):
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True


# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("✅ Проверить подписку", callback_data="check")
    markup.add(btn)

    text = "Чтобы получить доступ — подпишись на каналы:\n\n"
    for ch in CHANNELS:
        text += f"• {ch}\n"
    text += "\nПосле подписки нажми кнопку 👇"

    bot.send_message(message.chat.id, text, reply_markup=markup)


# Обработка кнопки
@bot.callback_query_handler(func=lambda call: call.data == "check")
def callback_check(call):
    user_id = call.from_user.id

    if check_subscription(user_id):
        bot.send_message(call.message.chat.id, f"✅ Подписка подтверждена!\nВот ссылка: {ACCESS_LINK}")
    else:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("✅ Проверить снова", callback_data="check")
        markup.add(btn)

        bot.send_message(
            call.message.chat.id,
            "❌ Ты ещё НЕ подписался на все каналы!\nПодпишись и попробуй снова.",
            reply_markup=markup
        )


# Запуск бота
if name == "main":
    print("✅ Бот запущен!")
    bot.polling(none_stop=True)
