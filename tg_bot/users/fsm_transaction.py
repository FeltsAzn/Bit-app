import telebot
from start_bot import bot
from http.client import HTTPException
from telebot.handler_backends import State, StatesGroup
import client
from exception_handler import connection_checker, exception_info


transaction_cache = dict()


class MyStates(StatesGroup):
    sender = State()
    receiver_address = State()
    amount = State()
    confirmation = State()


@bot.message_handler(
    func=lambda message: message.text == 'Перевести'
    or message.text == "Создать транзакцию"
)
def start_fsm(message):
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
    if message.text != 'Отмена создания транзакции':
        bot.send_message(message.chat.id, text="Подождите, проверяю баланс...")
        try:
            balance = connection_checker(response=client.get_user_balance(message.from_user.id))
        except ConnectionError | AttributeError | ValueError | HTTPException:
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
    else:
        transaction_cache.clear()
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton("Меню")
        markup.add(bnt)
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, text="Отмена транзакции", reply_markup=markup)


@bot.message_handler(state=MyStates.amount)
def amount_btc_without_fee(message):
    """
    Ввод количества валюты для перевода
    """
    if message.text != 'Отмена создания транзакции':
        bot.send_message(message.chat.id, text="Подождите, проверяю баланс...")
        try:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['amount'] = float(message.text)
        except ValueError:
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
    else:
        transaction_cache.clear()
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton("Меню")
        markup.add(bnt)
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, text="Отмена транзакции", reply_markup=markup)


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
        transaction_cache.clear()

    except (HTTPException, ConnectionError) as exception:
        exception_info(message=message,
                       http_mark_text="Меню",
                       conn_mark_text="Меню",
                       exception=exception)

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
    transaction_cache.clear()
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt = telebot.types.KeyboardButton("Меню")
    markup.add(bnt)
    bot.send_message(message.chat.id, text="Отмена транзакции.", reply_markup=markup)


