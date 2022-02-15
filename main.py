# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import ast
import datetime
import math
import random

import telebot
from peewee import DoesNotExist

from db import User, Insult, NameSynonims, NameSynonim, TextVariants, Info

# User.drop_table()
# User.create_table()
# NameSynonims.create_table()
# Insult.create_table()
# NameSynonim.create_table()
# TextVariants.create_table()
Info.create_table()
names = NameSynonims[1].names
bot = telebot.TeleBot('5206575629:AAGsZouQcdCdBNvQFCnfXhgSDDYNfhjSqEc')

"""admins = bot.get_chat_administrators(chat_id='-1001525196418')
for admin in admins:
    print(admin.user.id, admin.user.username, admin.user.first_name)
    strength = random.randint(40, 60)
    if not admin.user.is_bot:
        User.create(username=admin.user.username, first_name=admin.user.first_name, telegram_id=admin.user.id,
                    strength=strength)
"""


def generate_user_strength():
    admins = User.select()
    for admin in admins:
        admin.strength = random.randint(40, 60)
        admin.save()


# generate_user_strength()
# chatId = bot.chat_id
# Получение сообщений от юзера

@bot.message_handler(content_types=["text"])
def handle_text(message):
    if datetime.datetime.fromtimestamp(message.date + 120) < datetime.datetime.now():
        return
    chance = range(0, 3)
    words = message.text.lower().split(' ')

    if len(words) >= 3 and words[0] == 'дух' or words[0] == 'дух,':
        if words[1] + words[2] == 'топсилы':
            get_strength_top(message)
        if words[1] + words[2] in ['топвойны', 'топпобед']:
            get_wins_top(message)
        if words[1] + words[2] == 'топпоражений':
            get_loses_top(message)
        elif words[1] + words[2] == 'моясила':
            get_strength(message)
        elif words[1] + words[2] == 'топинфы':
            get_top_info(message)
        elif words[1] == 'инфа':
            get_info(message)
        return
    for word in words:
        roll = random.randint(0, 10)
        if word in names and len(word) > 3:
            if roll in chance:
                insult(word, message)
                return

        elif word == 'война' and message.reply_to_message:
            if message.reply_to_message.from_user.is_bot:
                bot.send_message(message.chat.id, get_phrase('attack on bot'))
                return
            duel(message.from_user.id, message.reply_to_message.from_user.id, message)

    # a = requests.post('localhost:8000/')


def get_phrase(name):
    try:
        phrase = random.choice(ast.literal_eval(TextVariants.get(TextVariants.name == name).text))
    except DoesNotExist:
        phrase = 'Дурак проебал бд'
    return phrase


def duel(attacker, defender, message):
    attacker = User.get(User.telegram_id == attacker)
    defender = User.get(User.telegram_id == defender)
    prize = round(random.uniform(0.0, 1.5), 1)
    if attacker.efficient_duels_count >= 25:
        prizeText = f'Приза не будет, *{attacker.first_name}* ' + get_phrase('no energy')
        prize = 0
    else:
        prizeText = f'Приз — {prize}силы💪'
    attacker.efficient_duels_count += 1
    if attacker.efficient_duels_count == 10:
        attacker.last_efficient_duel = datetime.datetime.now()
    chance = 50 + math.floor((attacker.strength - defender.strength) * 0.4)
    roll = random.randint(1, 100)

    text = f'Нападающий — *{attacker.first_name}* с силой {attacker.strength} \nЗащищающийся — *{defender.first_name}*' \
           f' с силой {defender.strength}\n'
    if roll in range(1, chance + 1):
        winner = attacker
        loser = defender
    else:
        winner = defender
        loser = attacker

    winner.strength = round(winner.strength + prize, 1)
    loser.strength = round(loser.strength - prize, 1)
    winner.wins += 1
    loser.loses += 1

    text = text + prizeText + f'\nПриз забирает *{winner.first_name}*🏆\nШанс на победу' \
                              f' атакующего был - {chance}% '
    winner.save()
    loser.save()

    bot.send_message(message.chat.id, text, parse_mode='Markdown')


def insult(name, message):
    try:
        user = NameSynonim.get(NameSynonim.name_synonims.contains(name)).user
    except DoesNotExist:
        print(name)
        return
    word = Insult.get(Insult.user == user)
    choice = random.choice(ast.literal_eval(word.insults))
    bot.send_message(message.chat.id, name + ' ' + choice)


def get_strength(message):
    user = User.get(User.telegram_id == message.from_user.id)
    if user.efficient_duels_count < 10:
        duels = f'Тебе доступны ещё {10 - user.efficient_duels_count} поединков сегодня'
    else:
        rest = datetime.timedelta(hours=8)
        time_since_last_duel = datetime.datetime.now().replace(microsecond=0) - datetime.datetime.strptime(
            user.last_efficient_duel.split('.')[0],
            "%Y-%m-%d %H:%M:%S")
        if rest > time_since_last_duel:
            duels = get_phrase('time to rest') + f' {rest - time_since_last_duel}'

        else:
            duels = get_phrase('rest completed')
            user.efficient_duels_count = 0
            user.save()
    bot.send_message(message.chat.id,
                     f'{user.first_name}, твоя сила - {user.strength}💪\nТвои победы - {user.wins}🏆\nТвои поражения - {user.loses}💀\n{duels}')


def get_wins_top(message):
    users = User.select().order_by(User.wins.desc())

    userList = []
    for user in users:
        a = {
            'wins': user.wins,
            'name': user.first_name
        }
        userList.append(a)
    top = f"Топ побед:\n🏆{userList[0]['name']} - {userList[0]['wins']}\n🥈{userList[1]['name']} -" \
          f" {userList[1]['wins']}\n🥉{userList[2]['name']} - {userList[2]['wins']} \n ----------------"
    for user in userList[3:]:
        top = top + f"\n{user['name']} - {user['wins']}"
    bot.send_message(message.chat.id, top)


def get_loses_top(message):
    users = User.select().order_by(User.loses.desc())

    userList = []
    for user in users:
        a = {
            'loses': user.loses,
            'name': user.first_name
        }
        userList.append(a)
    top = f"Топ поражений:\n⚰{userList[0]['name']} - {userList[0]['loses']}\n☠{userList[1]['name']} -" \
          f" {userList[1]['loses']}\n💀{userList[2]['name']} - {userList[2]['loses']} \n ----------------"
    for user in userList[3:]:
        top = top + f"\n{user['name']} - {user['loses']}"
    bot.send_message(message.chat.id, top)


def get_strength_top(message):
    users = User.select().order_by(User.strength.desc())

    userList = []
    for user in users:
        a = {
            'strength': user.strength,
            'name': user.first_name
        }
        userList.append(a)
    top = f"Топ силы:\n🏆{userList[0]['name']} - {userList[0]['strength']}\n🥈{userList[1]['name']} -" \
          f" {userList[1]['strength']}\n🥉{userList[2]['name']} - {userList[2]['strength']} \n ----------------"
    for user in userList[3:]:
        top = top + f"\n{user['name']} - {user['strength']}"
    bot.send_message(message.chat.id, top)


def get_info(message):
    percentage = round(random.uniform(0.0, 100.0), 1)
    try:
        if message.text[8] == ',':
            text = message.text[10:]
        else:
            text = message.text[9:]

        if text[0:3] != 'что':
            text = 'что ' + text
    except IndexError:
        bot.send_message(message.chat.id, 'Пошёл ты нахуй с такой инфой', parse_mode='Markdown')

    info, created = Info.get_or_create(text=text, defaults={'text': text, 'percentage': percentage})
    percentage = info.percentage
    reply = f'Инфа *{text}*? \n{get_phrase("info")}*{percentage}%*'
    bot.send_message(message.chat.id, reply, parse_mode='Markdown')


def get_top_info(message):
    infos = Info.select().limit(10).order_by(Info.percentage.desc())
    reply = 'Топ инфы в чате 🎲\n'
    for info in infos:
        reply = reply + f'\n{info.text[4:]} - {info.percentage}%'
    bot.send_message(message.chat.id, reply, parse_mode='Markdown')


# Запускаем бота
bot.polling(none_stop=True, interval=0)
