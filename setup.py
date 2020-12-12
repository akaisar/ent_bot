# /setup.py file
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# dependencies
import telebot
import os

from flask import Flask, request
from telebot import types

# bot initialization
token = os.getenv('API_BOT_TOKEN')
bot = telebot.TeleBot(token)


# start command handler
@bot.message_handler(commands=['start'])
def command_start_handler(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text='send location', request_location=True)
    markup.add(button_geo)
    bot.send_message(cid, 'Привет, здесь ты можешь бесплатно писать пробники ент', reply_markup=markup)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


# application entry point
# if __name__ == '__main__':
#     bot.polling(none_stop=True, interval=0)



# set webhook
server = Flask(__name__)


@server.route('/' + token, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv('HEROKU_URL') + token)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8443)))
