from datetime import datetime
import telebot
from telebot import types
import requests
import json
from bs4 import BeautifulSoup

bot = telebot.TeleBot('....')

url = 'https://admin.myfin.by/outer/informer/minsk/full' # url страницы
r = requests.get(url,headers={
"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
})
soup = BeautifulSoup(r.text,'html.parser')
items = soup.find_all('td',{'class':''})
bynusd = float(items[6].text)


btcusd = requests.get('https://blockchain.info/ticker').json()['USD']['15m']
#bynusd = requests.get('https://www.nbrb.by/api/exrates/rates?periodicity=0').json()[4]['Cur_OfficialRate']
bynbtc = int(bynusd * btcusd)


keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row( telebot.types.InlineKeyboardButton('6%',callback_data='1.06'),
              telebot.types.InlineKeyboardButton('7%',callback_data='1.07'))
keyboard.row( telebot.types.InlineKeyboardButton('8%',callback_data='1.08'),
              telebot.types.InlineKeyboardButton('9%',callback_data='1.09'))
keyboard.row( telebot.types.InlineKeyboardButton('10%',callback_data='1.10'),
              telebot.types.InlineKeyboardButton('11%',callback_data='1.11'))

value = ''
price = 0
res = 0

@bot.message_handler(commands=['start','go'])
def getMessage(message):
    bot.send_message(message.from_user.id,"How much you want nigga %",reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call:True)
def callback_func(query):
    global value, bynbtc
    data = query.data
    if 1.06 <= float(data) <= 1.11:
        value = eval(str(int(bynbtc * float(data))))
    else:
        print('Ошибка')
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value)
    bot.send_message(query.message.chat.id, 'Count:')
    bot.register_next_step_handler(query.message, number, value)

def number(message, value):
    if message.text.replace('.', '').isdigit():
        num = message.text
        result = int(float(num) * int(value) + 25)
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, 'I need count:')
        bot.register_next_step_handler(message, number, value)

bot.polling(none_stop=True, interval=0)
