import telebot
from telebot import types
import random

TOKEN = None

with open("token.txt") as f:
    TOKEN = f.read().strip()

bot = telebot.TeleBot(TOKEN)


def get_inline_markup():
    markup = types.InlineKeyboardMarkup(row_width=3)
    itembtn1 = types.InlineKeyboardButton('Камень', callback_data='камень')
    itembtn2 = types.InlineKeyboardButton('Ножницы', callback_data='ножницы')
    itembtn3 = types.InlineKeyboardButton('Бумага', callback_data='бумага')
    markup.add(itembtn1, itembtn2, itembtn3)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    markup = get_inline_markup()
    msg = bot.send_message(message.chat.id, "Привет! Давай поиграем в 'Камень, ножницы, бумага'! Выбери один из вариантов:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def game(call):
    user_choice = call.data
    bot_choice = random.choice(['камень', 'ножницы', 'бумага'])

    if user_choice == 'камень' or user_choice == 'ножницы' or user_choice == 'бумага':
        if user_choice == bot_choice:
            result = "Ничья! Мы выбрали одно и то же."
        elif (user_choice == 'камень' and bot_choice == 'ножницы') or (user_choice == 'ножницы' and bot_choice == 'бумага') or (user_choice == 'бумага' and bot_choice == 'камень'):
            result = f"Ты победил! Я выбрал {bot_choice}. Давай ещё разок?"
        else:
            result = f"Ты проиграл! Я выбрал {bot_choice}. Хочешь сыграть ещё?"
        bot.send_message(call.message.chat.id, result)
        bot.delete_message(call.message.chat.id, call.message.message_id - 0)  
        markup = get_inline_markup()
        bot.send_message(call.message.chat.id, "Выбери один из вариантов:", reply_markup=markup)

bot.polling()