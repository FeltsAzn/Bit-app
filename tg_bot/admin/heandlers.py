import math
from tg_bot.tg_bot_config import ADMIN_ID
from tg_bot import tg_bot_config
from tg_bot.start_bot import bot
import telebot
from tg_bot import client


counter = 0
database_cache = {}
users = {}


def admin_checker(message, text):
    if message.from_user.id in ADMIN_ID and message.text in text:
        return True
    return False


@bot.message_handler(func=lambda message: admin_checker(message, ("Админка", 'К списку пользователей')))
def admin_panel(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt1 = telebot.types.KeyboardButton("Общий баланс")
    btn2 = telebot.types.KeyboardButton("Все пользователи")
    btn3 = telebot.types.KeyboardButton("Закрыть админ-панель")
    markup.add(bnt1, btn2, btn3)
    text = f'Админ-панель'

    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(func=lambda message: admin_checker(message, ("Все пользователи",)))
def all_users(message):
    global users
    users = client.get_users()
    text = f"Пользователи: стр. {int(counter/5+1)}/{math.ceil(len(users['all_users'])/5)}"
    inline_markup = telebot.types.InlineKeyboardMarkup()
    for user in users['all_users'][:5]:
        inline_markup.add(
            telebot.types.InlineKeyboardButton(text=f'{user["id"]}.Пользователь: '
                                                    f'{user["nickname"] if user["nickname"] else user["tg_id"]}',
                                               callback_data=f'user_{user["id"]}'))
    btn = telebot.types.InlineKeyboardButton(text=">>>", callback_data='next-page')
    inline_markup.add(btn)
    bot.send_message(message.chat.id, text=text, reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'user')
def callback_query_user(call):
    for user in users['all_users']:
        user_id = call.data.split('_')[1]
        inline_markup = telebot.types.InlineKeyboardMarkup()
        if str(user["id"]) == user_id:
            user = client.get_info_about_user(user["id"])
            user_info = user["user_info"]
            inline_markup.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data='users'),
                              telebot.types.InlineKeyboardButton(text="Удалить пользователя",
                                                                 callback_data=f'delete_user_{user_id}'))
            count_sended_tran = len(user_info["wallet"]["sended_transactions"])
            count_received_tran = len(user_info["wallet"]["received_transactions"])
            bot.edit_message_text(text=f'Данные пользователя:\n'
                                       f'ID:   {user_info["id"]}\n'
                                       f'tg_id:   {user_info["tg_id"]}\n'
                                       f'Имя:   {user_info["nickname"]}\n'
                                       f'Админ:   {user_info["is_admin"]}\n'
                                       f'Баланс:   {user_info["wallet"]["balance"]}\n'
                                       f'Количество отправленных транзакции:   {count_sended_tran}\n'
                                       f'Количество принятых транзакции:   {count_received_tran}',
                                  chat_id=call.from_user.id,
                                  message_id=call.message.message_id,
                                  reply_markup=inline_markup)
            break


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'users')
def callback_query_users(call):
    """Возврат к отображению всех пользователей"""
    inline_markup = telebot.types.InlineKeyboardMarkup()
    for user in users['all_users'][counter:counter+5]:
        inline_markup.add(
            telebot.types.InlineKeyboardButton(text=f'{user["id"]}.Пользователь: '
                                                    f'{user["nickname"] if user["nickname"] else user["tg_id"]}',
                                               callback_data=f'user_{user["id"]}'))
    btn1 = telebot.types.InlineKeyboardButton(text="<<<", callback_data='previous-page')
    btn2 = telebot.types.InlineKeyboardButton(text=">>>", callback_data='next-page')
    inline_markup.add(btn1, btn2)
    bot.edit_message_text(text=f"Пользователи: стр. {int(counter/5+1)}/{math.ceil(len(users['all_users'])/5)}",
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'delete' and call.data.split('_')[1] == 'user')
def callback_query_delete(call):
    """Удаление пользователей"""
    user_id = int(call.data.split('_')[2])
    for i, user in enumerate(users["all_users"]):
        if str(user['id']) == user_id:
            client.delete_user(user_id)
            users["all_users"].pop(i)
    inline_markup = telebot.types.InlineKeyboardMarkup()
    for user in users['all_users'][counter:counter+5]:
        inline_markup.add(
            telebot.types.InlineKeyboardButton(text=f'{user["id"]}.Пользователь: '
                                                    f'{user["nickname"] if user["nickname"] else user["tg_id"]}',
                                               callback_data=f'user_{user["id"]}'))
    btn1 = telebot.types.InlineKeyboardButton(text="<<<", callback_data='previous-page')
    btn2 = telebot.types.InlineKeyboardButton(text=">>>", callback_data='next-page')
    inline_markup.add(btn1, btn2)
    bot.edit_message_text(text=f"Пользователи: стр. {int(counter/5+1)}/{math.ceil(len(users['all_users'])/5)}",
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'next-page')
def callback_query_next_page(call):
    """Следующая страница (если пользователей больше 5)"""
    global counter
    if counter+5 < len(users["all_users"]):
        counter += 5
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users['all_users'][counter:counter + 5]:
            inline_markup.add(
                telebot.types.InlineKeyboardButton(text=f'{user["id"]}.Пользователь: '
                                                        f'{user["nickname"] if user["nickname"] else user["tg_id"]}',
                                                   callback_data=f'user_{user["id"]}'))
        btn1 = telebot.types.InlineKeyboardButton(text="<<<", callback_data='previous-page')
        btn2 = telebot.types.InlineKeyboardButton(text=">>>", callback_data='next-page')
        inline_markup.add(btn1, btn2)
        bot.edit_message_text(
            text=f"Пользователи: стр. {int(counter / 5 + 1)}/{math.ceil(len(users['all_users']) / 5)}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline_markup)
    else:
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users['all_users'][counter:counter + 5]:
            inline_markup.add(
                telebot.types.InlineKeyboardButton(text=f'{user["id"]}.Пользователь: '
                                                        f'{user["nickname"] if user["nickname"] else user["tg_id"]}',
                                                   callback_data=f'user_{user["id"]}'))
        btn1 = telebot.types.InlineKeyboardButton(text="<<<", callback_data='previous-page')
        inline_markup.add(btn1)
        bot.edit_message_text(
            text=f"Пользователи: стр. {int(counter / 5 + 1)}/{math.ceil(len(users['all_users']) / 5)}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'previous-page')
def callback_query_previous_page(call):
    global counter
    if counter > 5:
        counter -= 5
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users['all_users'][counter:counter + 5]:
            inline_markup.add(
                telebot.types.InlineKeyboardButton(text=f'{user["id"]}.Пользователь: '
                                                        f'{user["nickname"] if user["nickname"] else user["tg_id"]}',
                                                   callback_data=f'user_{user["id"]}'))
        btn1 = telebot.types.InlineKeyboardButton(text="<<<", callback_data='previous-page')
        btn2 = telebot.types.InlineKeyboardButton(text=">>>", callback_data='next-page')
        inline_markup.add(btn1, btn2)
        bot.edit_message_text(
            text=f"Пользователи: стр. {int(counter / 5 + 1)}/{math.ceil(len(users['all_users']) / 5)}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline_markup)
    else:
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users['all_users'][counter:counter + 5]:
            inline_markup.add(
                telebot.types.InlineKeyboardButton(text=f'{user["id"]}.Пользователь: '
                                                        f'{user["nickname"] if user["nickname"] else user["tg_id"]}',
                                                   callback_data=f'user_{user["id"]}'))
        btn1 = telebot.types.InlineKeyboardButton(text=">>>", callback_data='next-page')
        inline_markup.add(btn1)
        bot.edit_message_text(
            text=f"Пользователи: стр. {int(counter / 5 + 1)}/{math.ceil(len(users['all_users']) / 5)}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline_markup)


@bot.message_handler(func=lambda message: admin_checker(message, "Общий баланс"))
def total_balance(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('К списку пользователей')
    markup.add(btn1)
    balance = client.total_balance()
    text = f'Общий баланс: {balance}'
    bot.send_message(message.chat.id, text, reply_markup=markup)


