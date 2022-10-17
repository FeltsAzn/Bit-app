from tg_bot.tg_bot_config import ADMIN_ID
from tg_bot.users.fsm_transaction import *


@bot.message_handler(commands=["start"])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt1 = telebot.types.KeyboardButton("Да, создать кошелек")
    btn2 = telebot.types.KeyboardButton("Нет, у меня уже есть кошелек")
    markup.add(bnt1, btn2)
    text = f'Привет, {message.from_user.full_name}, я крипто-кошелек!\n' \
           f'Через меня во можете хранить и отправлять криптовалюту.\n' \
           f'Хотите открыть кошелек?'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(
    func=lambda message: message.text == 'Меню'
    or message.text == "Закрыть админ-панель"
    or message.text == "Открыть кошелек"
    or message.text == "Отмена создания транзакции"
)
def menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt1 = telebot.types.KeyboardButton("Кошелек")
    btn2 = telebot.types.KeyboardButton("Перевести")
    btn3 = telebot.types.KeyboardButton("История")
    markup.add(bnt1, btn2, btn3)
    text = 'Выберите действие' if message.text != "Открыть кошелек" else 'Возвращение в меню'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(
    func=lambda message: message.text == "Попробовать обратиться снова"
)
def second_try(message):
    """Обработка повторной попытки получения нового кошелька или старого кошелька"""
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt1 = telebot.types.KeyboardButton("Да, создать кошелек")
    btn2 = telebot.types.KeyboardButton("Нет, у меня уже есть кошелек")
    markup.add(bnt1, btn2)
    text = f'Привет, {message.from_user.full_name}, я крипто-кошелек!\n' \
           f'Попробуем снова?\n' \
           f'Хотите открыть кошелек?'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(
    func=lambda message: message.text == 'Да, создать кошелек'
    or message.text == 'Попробовать создать кошелек'
)
def create_user(message):
    """Обработка пользователя, который хочет создать новый кошелек"""
    try:
        connection_checker(response=client.create_user(
            {"tg_id": message.from_user.id,
             "nickname": message.from_user.username,
             "is_admin": message.from_user.id in ADMIN_ID}))

    except (HTTPException, ConnectionError) as ex:
        exception_info(message=message,
                       http_mark_text="Попробовать создать кошелек",
                       conn_mark_text="Попробовать обратиться снова",
                       exception=ex)

    except ValueError:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton("Найти мой кошелек")
        markup.add(bnt)
        text = f'Ой, что-то пошло не так :(\n' \
               f'Похоже у вас уже есть кошелек, попробуйте найти его.\n'
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)

    else:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton("Открыть кошелек")
        markup.add(bnt)
        text = f'Кошелек успешно создан!'
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(
    func=lambda message: message.text == "Нет, у меня уже есть кошелек"
    or message.text == 'Найти мой кошелек'
)
def check_user(message):
    """Обработка пользователя, который хочет найти уже созданный кошелек"""
    try:
        tg_id = message.from_user.id
        connection_checker(response=client.get_user_by_tg(tg_id=tg_id))

    except (HTTPException, ConnectionError) as ex:
        exception_info(message=message,
                       http_mark_text="Попробовать обратиться снова",
                       conn_mark_text="Попробовать обратиться снова",
                       exception=ex)

    except AttributeError:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton("Попробовать создать кошелек")
        markup.add(bnt)
        text = f'К сожалению, я не нашел ваш кошелек:(\n' \
               f'Создайте новый кошелек'
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)

    else:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton("Открыть кошелек")
        markup.add(bnt)
        text = f'Да, я нашел ваш кошелек!'
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(regexp='Кошелек')
def wallet(message):
    bot.send_message(chat_id=message.chat.id, text="Подождите...")
    try:
        tg_id = message.from_user.id
        balance = connection_checker(response=client.get_user_balance(tg_id=tg_id))

    except (HTTPException, ConnectionError) as ex:
        exception_info(message=message,
                       http_mark_text="Меню",
                       conn_mark_text="Меню",
                       exception=ex)

    else:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton("Меню")
        markup.add(bnt)
        text = f'Ваш баланс: {balance["balance"]}'
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(regexp='История')
def history(message):
    bot.send_message(chat_id=message.chat.id, text="Подождите...")
    try:
        tg_id = message.from_user.id
        transactions = connection_checker(client.get_user_transactions(tg_id=tg_id))

    except (HTTPException, ConnectionError) as ex:
        exception_info(message=message,
                       http_mark_text="Меню",
                       conn_mark_text="Меню",
                       exception=ex)

    except AttributeError:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt1 = telebot.types.KeyboardButton("Создать транзакцию")
        bnt2 = telebot.types.KeyboardButton("Меню")
        markup.add(bnt1, bnt2)
        text = f'К сожалению, у вас еще нет транзакций\n' \
               f'Хотите создать транзацкию?'
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)

    else:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton("Меню")
        markup.add(bnt)
        text = f'Ваши транзакции:\n' \
               f'{transactions["transactions"]["sended_transactions"]}\n' \
               f'{transactions["transactions"]["received_transactions"]}'
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)



