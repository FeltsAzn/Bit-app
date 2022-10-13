import math

from tg_bot import config
from tg_bot.start_bot import bot
import telebot

users = config.fake_database['users']
counter = 0
database_cache = {}


def admin_checker(message, text):
    if message.from_user.id == config.ADMIN_ID and message.text == text:
        return True
    return False


@bot.message_handler(func=lambda message: admin_checker(message, "Админка"))
def admin_panel(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt1 = telebot.types.KeyboardButton("Общий баланс")
    btn2 = telebot.types.KeyboardButton("Все пользователи")
    btn3 = telebot.types.KeyboardButton("Данные по пользователю")
    btn4 = telebot.types.KeyboardButton("Удалить пользователя")
    btn5 = telebot.types.KeyboardButton("Закрыть админ-панель")
    markup.add(bnt1, btn2, btn3, btn4, btn5)
    text = f'Админ-панель'

    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(func=lambda message: admin_checker(message, "Все пользователи"))
def all_users(message):
    text = f"Пользователи: стр. {int(counter/5+1)}/{math.ceil(len(users)/5)}"
    inline_markup = telebot.types.InlineKeyboardMarkup()
    for user in users[:5]:
        inline_markup.add(telebot.types.InlineKeyboardButton(text=f'Пользователь: {user["name"]}',
                                                             callback_data=f'user_{user["id"]}'))
    btn = telebot.types.InlineKeyboardButton(text=">>>", callback_data='next-page')
    inline_markup.add(btn)
    bot.send_message(message.chat.id, text=text, reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'user')
def callback_query_user(call):
    global counter
    for user in users:
        user_id = call.data.split('_')[1]
        inline_markup = telebot.types.InlineKeyboardMarkup()
        if str(user["id"]) == user_id:
            inline_markup.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data='users'),
                              telebot.types.InlineKeyboardButton(text="Удалить пользователя",
                                                                 callback_data=f'delete_user_{user_id}'))
            bot.edit_message_text(text=f'Данные пользователя:\n'
                                       f'ID: {user["id"]}'
                                       f'Имя: {user["name"]}'
                                       f'Ник: {user["nick"]}'
                                       f'Баланс: {user["balance"]}',
                                  chat_id=call.from_user.id,
                                  message_id=call.message.message_id,
                                  reply_markup=inline_markup)
            break


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'users')
def callback_query_users(call):
    inline_markup = telebot.types.InlineKeyboardMarkup()
    for user in users[counter:counter+5]:
        inline_markup.add(telebot.types.InlineKeyboardButton(text=f'Пользователь: {user["name"]}',
                                                             callback_data=f"user-{user['id']}"))
    btn1 = telebot.types.InlineKeyboardButton(text="<<<", callback_data='previous-page')
    btn2 = telebot.types.InlineKeyboardButton(text=">>>", callback_data='next-page')
    inline_markup.add(btn1, btn2)
    bot.edit_message_text(text=f"Пользователи: стр. {int(counter/5+1)}/{math.ceil(len(users)/5)}",
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'delete' and call.data.split('_')[1] == 'user')
def callback_query_delete(call):
    global counter
    user_id = int(call.data.split('_')[2])
    for i, user in enumerate(users):
        if user['id'] == user_id:
            users.pop(i)
    inline_markup = telebot.types.InlineKeyboardMarkup()
    for user in users[counter:counter+5]:
        inline_markup.add(telebot.types.InlineKeyboardButton(text=f"Пользователь: {user['name']}",
                                                             callback_data=f'user_{user["id"]}'))
    btn1 = telebot.types.InlineKeyboardButton(text="<<<", callback_data='previous-page')
    btn2 = telebot.types.InlineKeyboardButton(text=">>>", callback_data='next-page')
    inline_markup.add(btn1, btn2)
    bot.edit_message_text(text=f"Пользователи: стр. {int(counter/5+1)}/{math.ceil(len(users)/5)}",
                          chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'next-page')
def callback_query_next_page(call):
    global counter
    if counter+5 < len(users):
        counter += 5
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users[counter:counter+5]:
            inline_markup.add(telebot.types.InlineKeyboardButton(text=f"Пользователь: {user['name']}",
                                                                 callback_data=f'user_{user["id"]}'))
        btn1 = telebot.types.InlineKeyboardButton(text="<<<", callback_data='previous-page')
        btn2 = telebot.types.InlineKeyboardButton(text=">>>", callback_data='next-page')
        inline_markup.add(btn1, btn2)
        bot.edit_message_text(text=f"Пользователи: стр. {int(counter/5+1)}/{math.ceil(len(users)/5)}",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup)
    else:
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users[counter:counter + 5]:
            inline_markup.add(telebot.types.InlineKeyboardButton(text=f"Пользователь: {user['name']}",
                                                                 callback_data=f'user_{user["id"]}'))
        btn = telebot.types.InlineKeyboardButton(text="<<<", callback_data='previous-page')
        inline_markup.add(btn)
        bot.edit_message_text(text=f"Пользователи: стр. {int(counter/5+1)}/{math.ceil(len(users)/5)}",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'previous-page')
def callback_query_previous_page(call):
    global counter
    if counter > 5:
        counter -= 5
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users[counter:counter+5]:
            inline_markup.add(telebot.types.InlineKeyboardButton(text=f"Пользователь: {user['name']}",
                                                                 callback_data=f'user_{user["id"]}'))
        btn1 = telebot.types.InlineKeyboardButton(text="<<<", callback_data='previous-page')
        btn2 = telebot.types.InlineKeyboardButton(text=">>>", callback_data='next-page')
        inline_markup.add(btn1, btn2)
        bot.edit_message_text(text=f"Пользователи: стр. {int(counter/5+1)}/{math.ceil(len(users)/5)}",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup)
    else:
        counter -= 5
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users[counter:counter+5]:
            inline_markup.add(telebot.types.InlineKeyboardButton(text=f"Пользователь: {user['name']}",
                                                                 callback_data=f'user_{user["id"]}'))
        btn = telebot.types.InlineKeyboardButton(text=">>>", callback_data='next-page')
        inline_markup.add(btn)
        bot.edit_message_text(text=f"Пользователи: стр. {int(counter/5+1)}/{math.ceil(len(users)/5)}",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup)


@bot.message_handler(func=lambda message: admin_checker(message, "Общий баланс"))
def total_balance(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')
    btn2 = telebot.types.KeyboardButton('Админка')
    markup.add(btn1, btn2)
    balance = 0
    for user in users:
        balance += user['balance']
    text = f'Общий баланс: {balance}'
    bot.send_message(message.chat.id, text, reply_markup=markup)


