# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import random

import telebot
from db import User

counter = []
bot = telebot.TeleBot('5206575629:AAGsZouQcdCdBNvQFCnfXhgSDDYNfhjSqEc')

User.create_table()
admins = bot.get_chat_administrators(chat_id='-1001525196418')
for admin in admins:
    print(admin.user.id, admin.user.username, admin.user.first_name)
#chatId = bot.chat_id
# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    #chance = range(0, 5)
    chance = (-1,0)
    #bot.send_message(message.chat.id, 'тестируем свита-алкаша ')
    #print(message.chat)
    roll = random.randint(0, 10)
    if roll in chance:
        if 'крок' in message.text.lower():
            choice = random.choice(['вох', 'каблук', 'гандон', 'чорт', 'хуй соси', 'козёл'])
            bot.send_message(message.chat.id, 'крок ' + choice)
        elif 'свит' in message.text.lower():
            choice = random.choice(['алкаш', 'титёк', 'гандон', 'уродец', 'старпер'])
            bot.send_message(message.chat.id, 'свит ' + choice )
        elif 'димка' in message.text.lower():
            choice = random.choice(['7 см', 'говноед', 'электрик', 'чорт', 'титька', 'москвич'])
            bot.send_message(message.chat.id, 'димка ' + choice)
        elif 'соня' in message.text.lower():
            choice = random.choice(['скинь попу', 'истеричка', 'сучка', 'вох'])
            bot.send_message(message.chat.id, 'соня ' + choice)
        elif 'егорка' in message.text.lower():
            bot.send_message(message.chat.id, 'егорка молодец')
        else:
            pass
    # a = requests.post('localhost:8000/')



# Запускаем бота
bot.polling(none_stop=True, interval=0)