from tg_bot import config
from tg_bot.start_bot import bot
import telebot

users = config.fake_database['users']


@bot.message_handler(
    func=lambda message: message.from_user.id == config.ADMIN_ID and message.text == "Админка")
def admin_panel(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt1 = telebot.types.KeyboardButton("Общий баланс")
    btn2 = telebot.types.KeyboardButton("Все пользователи")
    btn3 = telebot.types.KeyboardButton("Данные по пользователю")
    btn4 = telebot.types.KeyboardButton("Удалить пользователя")
    markup.add(bnt1, btn2, btn3, btn4)
    text = f'Привет, {message.from_user.full_name}, админ-панель активирована.'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(
    func=lambda message: message.from_user.id == config.ADMIN_ID and message.text == "Все пользователи")
def all_users(message):
    text = 'Пользователи:'
    inline_markup = telebot.types.InlineKeyboardMarkup()
    for user in users:
        inline_markup.add(telebot.types.InlineKeyboardButton(text=f'Пользователь: {user["name"]}',
                                                             callback_data=f'user_{user["id"]}'))
    bot.send_message(message.chat.id, text=text, reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    query_type = call.data.split('_')[0]
    if query_type == 'user':
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
    elif query_type == 'users':
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users:
            inline_markup.add(telebot.types.InlineKeyboardButton(text=f'Пользователь: {user["name"]}',
                                                                 callback_data=f"user_{user['id']}"))
        bot.edit_message_text(text="Пользователи:",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup)
    elif query_type == 'delete' and call.data.split('_')[1] == 'user':
        user_id = int(call.data.split('_')[2])
        for i, user in enumerate(users):
            if user['id'] == user_id:
                users.pop(i)
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users:
            inline_markup.add(telebot.types.InlineKeyboardButton(text=f"Пользователь: {user['name']}",
                                                                 callback_data=f'user_{user["id"]}'))
        bot.edit_message_text(text="Пользователи:",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup)


@bot.message_handler(func=lambda message: message.from_user.id == config.ADMIN_ID and message.text == "Общий баланс")
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



