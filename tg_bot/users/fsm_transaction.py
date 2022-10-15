import telebot  # telebot
from tg_bot.start_bot import bot
from http.client import HTTPException
from telebot.handler_backends import State, StatesGroup
from .. import client# States

# States storage
from telebot.storage import StateMemoryStorage

# Starting from version 4.4.0+, we support storages.
# StateRedisStorage -> Redis-based storage.
# StatePickleStorage -> Pickle-based storage.
# For redis, you will need to install redis.
# Pass host, db, password, or anything else,
# if you need to change config for redis.
# Pickle requires path. Default path is in folder .state-saves.
# If you were using older version of pytba for pickle,
# you need to migrate from old pickle to new by using
# StatePickleStorage().convert_old_to_new()
transaction_cache = dict()


def connection_checker(response):
    if 'db_error' in response.keys():
        raise ConnectionError(f"{response['db_error']}")
    elif "not_found" in response.keys():
        raise AttributeError(f"{response['not_found']}")
    elif "db_data_error" in response.keys():
        raise TypeError(f"{response['db_data_error']}")
    elif "server_error" in response.keys():
        raise HTTPException(f"{response['server_error']}")
    else:
        return response


class MyStates(StatesGroup):
    # Just name variables differently  # creating instances of State class is enough from now
    sender = State()
    receiver_address = State()
    amount = State()
    confirmation = State()


# Now, you can pass storage to bot.
# States group.


@bot.message_handler(
    func=lambda message: message.text == 'Перевести'
    or message.text == "Создать транзакцию"
)
def start_ex(message):
    """Получем информацию об отправителе, входим в машину состояния"""
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt = telebot.types.KeyboardButton("Отмена создания транзакции")
    markup.add(bnt)
    bot.set_state(message.from_user.id, MyStates.receiver_address, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['sender'] = message.from_user.id
    bot.send_message(message.chat.id, text='Введите адрес кошелька куда хотите перевести:', reply_markup=markup)


@bot.message_handler(state=MyStates.receiver_address)
def receiver_address(message):
    """
    Ввод адреса получателя
    """
    bot.send_message(message.chat.id, text="Подождите, проверяю баланс...")
    try:
        balance = connection_checker(response=client.get_user_balance(message.from_user.id))
    except ConnectionError | AttributeError | TypeError | HTTPException:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton("Меню")
        markup.add(bnt)
        bot.send_message(message.chat.id, text="Ошибка транзакции, попробуйте перевести позже", reply_markup=markup)
        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.chat.id, f"Количество валюты, которую хотите отправить:\n"
                                          f"Ваш баланс {balance['balance']}")
        bot.set_state(message.from_user.id, MyStates.amount, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['receiver_address'] = message.text


@bot.message_handler(state=MyStates.amount)
def amount_btc_without_fee(message):
    """
    Ввод количества валюты для перевода
    """
    try:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['amount'] = float(message.text)
    except ValueError:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt1 = telebot.types.KeyboardButton("Нет, отказываюсь")
        bnt2 = telebot.types.KeyboardButton("Да, подтверждаю")
        markup.add(bnt1, bnt2)
        text = "Введенное количество неверно!\n" \
               "Введите число!"
        bot.send_message(message.chat.id, text=text)

    else:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt1 = telebot.types.KeyboardButton("Нет, отказываюсь")
        bnt2 = telebot.types.KeyboardButton("Да, подтверждаю")
        markup.add(bnt1, bnt2)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            msg = ("Данные транзакции\n<b>"
                   f"Данные отправителя: {message.from_user.full_name}\n"
                   f"Адрес отправления: {data['receiver_address']}\n"
                   f"Количество валюты: {data['amount']}</b>")
            transaction_cache["sender_tg_id"] = data['sender']
            transaction_cache["receiver_address"] = data['receiver_address']
            transaction_cache["amount_btc_without_fee"] = data['amount']
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, text=msg, reply_markup=markup, parse_mode="html")


@bot.message_handler(
    func=lambda message: message.text == "Да, подтверждаю"
)
def confirm_transaction(message):
    """
    Подтверждение транзакции
    """
    bot.send_message(message.chat.id, text="Отправляю транзакцию...")
    try:
        transaction = connection_checker(client.create_transaction(transaction_cache))
        print(transaction)
    except HTTPException:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton("Меню")
        markup.add(bnt)
        text = f'Ой, что-то пошло не так :(\n' \
               f'Возможно сервер не отвечает.\n' \
               f'Попробуйте создать транзакцию чуть позже'
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)

    except ConnectionError:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton("Меню")
        markup.add(bnt)
        text = f'Ой, что-то пошло не так :(\n' \
               f'Попробуйте обратиться позже.'
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)

    except TypeError:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt1 = telebot.types.KeyboardButton("Создать транзакцию")
        btn2 = telebot.types.KeyboardButton("Меню")
        markup.add(bnt1, btn2)
        text = f'Неправильно введены данные транзакции\n' \
               f'Хотите создать новую транзакцию?\n'
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
    else:
        if "failed" in transaction:
            text = "Ошибка транзакции.\n" \
                   "Недостаточно средств на вашем счете."
        else:
            text = "Транзакция совершена успешно."
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton("Меню")
        markup.add(bnt)

        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(
    func=lambda message: message.text == "Отмена создания транзакции"
    or message.text == "Нет, отказываюсь"
)
def cancel_transaction(message):
    """
    Отмена транзакции
    """
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt = telebot.types.KeyboardButton("Меню")
    markup.add(bnt)
    bot.send_message(message.chat.id, text="Отмена транзакции.", reply_markup=markup)
