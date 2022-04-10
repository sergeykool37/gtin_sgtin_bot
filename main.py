import telebot, os
from dotenv import load_dotenv
import os

load_dotenv()
token_bot = os.environ.get('TOKEN_BOT')
bot = telebot.TeleBot(token_bot)

@bot.message_handler(commands=['start'])
def start(m, res = False):
    bot.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь )')

@bot.message_handler(content_types=["text"])
def handle_text(message):
    text = message.text
    if len(text) == 85:
        gtin_sgtin = text[2:17] + text[19:32]
        bot.send_message(message.chat.id, gtin_sgtin)

bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    print('hi')


