import telebot, os
import config
import getInfoSgtinForBot


token_bot =config.BOT_TOKEN
bot = telebot.TeleBot(token_bot)

@bot.message_handler(commands=['start'])
def start(m, res = False):
    bot.send_message(m.chat.id, 'Я на связи. Oтправь datamatrix ')

@bot.message_handler(content_types=["text"])
def handle_text(message):
    text = message.text
    if len(text) == 85:
        gtin_sgtin = text[2:16] + text[18:31]
        bot.send_message(message.chat.id, gtin_sgtin)
        try:
            info_sgtin = getInfoSgtinForBot.get_message_for_bot(gtin_sgtin)
            bot.send_message(message.chat.id, info_sgtin)
        except Exception:
            bot.send_message(message.chat.id, 'ошибка при получении данных')

    elif len(text) == 27:
        gtin_sgtin = text
        try:
            info_sgtin = getInfoSgtinForBot.get_message_for_bot(gtin_sgtin)
            bot.send_message(message.chat.id, info_sgtin)
        except Exception:
            bot.send_message(message.chat.id, 'ошибка при получении данных')






bot.polling(none_stop=True, interval=0)




