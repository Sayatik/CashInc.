import telebot
import const
from telebot import types


bot = telebot.TeleBot(const.API_TOKEN)


markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_address = types.KeyboardButton('Our address: ',request_location=True)
btn_payment = types.KeyboardButton('Payment methods')
btn_delivery = types.KeyboardButton('Delivery methods')
markup_menu.add(btn_address, btn_payment, btn_delivery)

markup_inline_payment = types.InlineKeyboardMarkup()
btn_in_cash = types.InlineKeyboardButton('Cash', callback_data='cash')
btn_in_card = types.InlineKeyboardButton('Kaspi Gold', callback_data='kaspi gold')
markup_inline_payment.add(btn_in_cash, btn_in_card)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Hi, we are Cash inc. ;)", reply_markup = markup_menu)

@bot.message_handler(func=lambda message: True)

def echo_all(message):
    print(message)
    if message.text == 'Delivery methods':
        bot.reply_to(message, 'Online ticket', reply_markup = markup_menu)
    elif message.text == 'Payment methods':
        bot.reply_to(message, 'We have 2 methods of Payment: ', reply_markup=markup_inline_payment)
    else :
        bot.reply_to(message, message.text, reply_markup=markup_menu)

@bot.message_handler(func=lambda message: True, content_types= ['location'])
def store_location(message):
    print(message)
    lon = message.location.longitude
    lat = message.location.latitude
    print('Longitude {}, Latitude {}'.format(lon, lat))

@bot.callback_query_handler(func=lambda call:True)
def callback_payment(call):
    print(call)
    if call.data =='cash':
        bot.send_message(call.message.chat.id, text="""
        You can pay cash in front of our RedCanteen, so u will take your ticket there.
        """, reply_markup=markup_inline_payment)
    elif call.data =='kaspi gold':
        bot.send_message(call.message.chat.id, text="""
        You can send money by Phone number, which is chained with my KaspiGold:
        87026479903
        """, reply_markup=markup_inline_payment)


bot.polling()
