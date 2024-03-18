import os

import telebot

from map_data import main

BOT_TOKEN = os.environ.get('bot_token')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "I'm Gmap Vigilante i can provide you a excel of an google search results.")
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "Processing your results...")
    q=message.text
    main(q)
    bot.reply_to(message, "Your Results Processed.")
    bot.send_document(chat_id=message.chat.id, document=open(f"./{q}.xlsx",'rb').read(),caption="Gmap data for you for issues cantact developer in connectwithsanthosh@gmail.com (or) devsanthoshmk at github",visible_file_name=f"{q}.xlsx")
    os.remove(f"./{q}.xlsx")
bot.infinity_polling()