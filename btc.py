from datetime import datetime
import telebot
from telebot import types
import requests
import json

bot = telebot.TeleBot('....')

a = requests.get('https://blockchain.info/ticker').json()
btcusd = a['USD']['15m']
b = requests.get('https://www.nbrb.by/api/exrates/rates?periodicity=0').json()
bynusd= (b[4]['Cur_OfficialRate'])

bynbtc = int(bynusd * btcusd)

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row( telebot.types.InlineKeyboardButton('4%',callback_data='1.04'),
              telebot.types.InlineKeyboardButton('5%',callback_data='1.05'))
keyboard.row( telebot.types.InlineKeyboardButton('6%',callback_data='1.06'),
              telebot.types.InlineKeyboardButton('7%',callback_data='1.07'))
keyboard.row( telebot.types.InlineKeyboardButton('8%',callback_data='1.08'),
              telebot.types.InlineKeyboardButton('9%',callback_data='1.09'))

value = ''
price = 0
res = 0

@bot.message_handler(commands=['start','go'])
def getMessage(message):
    bot.send_message(message.from_user.id,"%",reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call:True)
def callback_func(query):
    global value, bynbtc
    data = query.data
    if data == '1.04':
        value = eval(str(int(bynbtc * float(data))))
    elif data == '1.05':
        value = eval(str(int(bynbtc * float(data))))
    elif data == '1.06':
        value = eval(str(int(bynbtc * float(data))))
    elif data == '1.07':
        value = eval(str(int(bynbtc * float(data))))
    elif data == '1.08':
        value = eval(str(int(bynbtc * float(data))))
    elif data == '1.09':
        value = eval(str(int(bynbtc * float(data))))
    else:
        pass
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value)
    bot.send_message(query.message.chat.id, 'Count:')
    bot.register_next_step_handler(query.message, number, value)

def number(message, value):
    if message.text.replace('.', '').isdigit():
        num = message.text
        result = int(float(num) * int(value) + 8)
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, 'I need count:')
        bot.register_next_step_handler(message, number, value)

bot.polling(none_stop=True, interval=0)
