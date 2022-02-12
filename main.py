# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import ast
import datetime
import math
import random

import telebot
from db import User, Insult, NameSynonims, NameSynonim

# User.drop_table()
# User.create_table()
# NameSynonims.create_table()
# Insult.create_table()
# NameSynonim.create_table()
names = NameSynonims[1].names
bot = telebot.TeleBot('5206575629:AAGsZouQcdCdBNvQFCnfXhgSDDYNfhjSqEc')

"""admins = bot.get_chat_administrators(chat_id='-1001525196418')
for admin in admins:
    print(admin.user.id, admin.user.username, admin.user.first_name)
    strength = random.randint(40, 60)
    User.create(username=admin.user.username, first_name=admin.user.first_name, telegram_id=admin.user.id, strength=strength)"""


# chatId = bot.chat_id
# Получение сообщений от юзера

@bot.message_handler(content_types=["text"])
def handle_text(message):
    if datetime.datetime.fromtimestamp(message.date + 120) < datetime.datetime.now():
        return
    chance = range(0, 5)
    # chance = (-1, 0)
    # bot.send_message(message.chat.id, 'тестируем свита-алкаша ')
    # print(message.chat)
    # print(message.reply_to_message.from_user)

    words = message.text.lower().split(' ')

    if len(words)>=3 and words[0] == 'дух' or words[0] == 'дух,':
        if words[1] + words[2] == 'топсилы':
            get_strength_top(message)
        elif words[1] + words[2] == 'моясила':
            get_strength(message)
        return
    for word in words:
        roll = random.randint(0, 10)
        if word in names and len(word) > 3:
            if roll in chance:
                insult(word, message)
                return

        elif word == 'война' and message.reply_to_message:
            duel(message.from_user.id, message.reply_to_message.from_user.id, message)

    # a = requests.post('localhost:8000/')


def duel(attacker, defender, message):
    attacker = User.get(User.telegram_id == attacker)
    defender = User.get(User.telegram_id == defender)
    chance = 50 + math.floor((attacker.strength - defender.strength) * 0.4)
    roll = random.randint(1, 100)
    prize = round(random.uniform(0.0, 1.5), 1)
    print(prize)
    if roll in range(1, chance + 1):
        attacker.strength = attacker.strength + prize
        defender.strength = defender.strength - prize
        winner = attacker.first_name
    else:
        attacker.strength = attacker.strength - prize
        defender.strength = defender.strength + prize
        winner = defender.first_name

    text = f'Нападающий — *{attacker.first_name}* с силой {attacker.strength} \nЗащищающийся — *{defender.first_name}*' \
           f' с силой {defender.strength}\nПриз — {prize} силы 💪\nПриз забирает {winner}\nШанс на победу' \
           f' атакующего был - {chance}% '
    attacker.save()
    defender.save()
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


def insult(name, message):
    user = NameSynonim.get(NameSynonim.name_synonims.contains(name)).user
    word = Insult.get(Insult.user == user)
    choice = random.choice(ast.literal_eval(word.insults))
    bot.send_message(message.chat.id, name + ' ' + choice)


def get_strength(message):
    user = User.get(User.telegram_id == message.from_user.id)
    bot.send_message(message.chat.id, f'{user.first_name}, твоя сила - {user.strength}💪')


def get_strength_top(message):
    users = User.select().order_by(User.strength.desc())

    userList = []
    for user in users:
        a = {
            'strength': user.strength,
            'name': user.first_name
        }
        userList.append(a)
    top = f"Топ силы:\n{userList[0]['name']} - {userList[0]['strength']}\n{userList[1]['name']} -" \
          f" {userList[1]['strength']}\n{userList[2]['name']} - {userList[2]['strength']} \n ----------------"
    for user in userList[3:]:
        top = top + f"\n{user['name']} - {user['strength']}"
    bot.send_message(message.chat.id, top)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
