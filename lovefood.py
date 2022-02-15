import telebot
from telebot import types
import json
import pandas as pd
import re

columns = ['page', 'type', 'name', 'ingredients', 'measure']
data = pd.read_csv('recipies_new.csv', sep='\t', names=columns)

with open('salt_list', 'r', encoding='utf-8') as f:
	frequent_pairs =  json.loads(f.read())

bot = telebot.TeleBot('5240440426:AAF3hXn4H9R7RHG7i1V3D5uuOy3R_OnQdGc')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'Привет')

@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Ингридиенты")
    item2 = types.KeyboardButton('Наиболее частые сочетания')
    markup.add(item1, item2)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)

def get_recepies(ingr):
    ingridients = data.groupby('name').agg({"ingredients": list}).reset_index()

    new_ingr = []
    for i in ingridients['ingredients']:
        new_i = []
        for one in i:
            new_i.append(one.lower())
        new_ingr.append(new_i)

    ingridients["ingredients_lower"] = new_ingr

    answer = []
    for i, row in ingridients.iterrows():
        count = 0
        for one in ingr:
            if one in row['ingredients_lower']:
                count += 1
        if count == len(ingr):
            if len(answer) < 5:
                answer.append(row['name'])
            else:
                break

    return answer

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Ингридиенты":
        bot.send_message(message.chat.id, 'Введите нужные ингридиенты')
    elif message.text=="Наиболее частые сочетания":
        message_pairs = '\n'.join([list(k.keys())[0] for k in frequent_pairs[:5]])
        bot.send_message(message.chat.id, message_pairs)
    else:
        list_of_ingridients = re.sub(r'[^\w\s]', '', message.text.lower()).split()
        recepies = get_recepies(list_of_ingridients)
        bot.send_message(message.chat.id, '\n'.join(recepies))

bot.polling()
