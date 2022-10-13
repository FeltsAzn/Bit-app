import telebot
from pony.orm import IntegrityError

from tg_bot.start_bot import bot
from .. import client


@bot.message_handler(commands=["start"])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt1 = telebot.types.KeyboardButton("Да, создать кошелек")
    btn2 = telebot.types.KeyboardButton("Нет, у меня уже есть")
    markup.add(bnt1, btn2)
    text = f'Привет, {message.from_user.full_name}, я крипто-кошелёк!\n' \
           f'ты можешь хранить и отправлять криптовалюту.\n' \
           f'Хочешь открыть кошелек?'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(
    func=lambda message: message.text == 'Да, создать кошелек' or message.text == 'Попробовать создать кошелек')
def create_user(message):
    try:
        new_user = client.create_user(
            {"tg_id": message.from_user.id,
             "nickname": message.from_user.username})
    except Exception:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton("Попробовать создать кошелек")
        markup.add(bnt)
        text = f'Ой, что-то пошло не так :(\n' \
               f'Возможно сервер не отвечает.\n' \
               f'Попробуйте создать чуть позже'
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
    else:
        if new_user.status_code == 200:
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            bnt = telebot.types.KeyboardButton("Открыть кошелек")
            markup.add(bnt)
            text = f'Кошелек успешно создан!'
            bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
        elif new_user.status_code == 500:
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            bnt1 = telebot.types.KeyboardButton("Попробовать создать кошелек")
            bnt2 = telebot.types.KeyboardButton("Найти мой кошелек")
            markup.add(bnt1, bnt2)
            text = f'Ой, что-то пошло не так :(\n' \
                   f'Возможно у вас уже есть кошелек?\n' \
                   f'Если у вас нет кошелька, то попробуйте создать чуть позже'
            bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(
    func=lambda message: message.text == "Нет, у меня уже есть" or message.text == 'Найти мой кошелек')
def check_user(message):
    response = client.get_user_by_tg(message.from_user.id)
    print(response)
    if response['user']:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton("Открыть кошелек")
        markup.add(bnt)
        text = f'Да, я нашел ваш кошелек!'
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
    else:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton("Попробовать создать кошелек")
        markup.add(bnt)
        text = f'Извините, я не смог найти ваш кошелек :(\n' \
               f'Создайте новый кошелек!'
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(regexp="Открыть кошелек")
def check_user(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt1 = telebot.types.KeyboardButton("Кошелек")
    btn2 = telebot.types.KeyboardButton("Перевести")
    btn3 = telebot.types.KeyboardButton("История")
    markup.add(bnt1, btn2, btn3)
    text = f'Открываем кошелек'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(regexp='Кошелек')
def wallet(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt1 = telebot.types.KeyboardButton("Меню")
    markup.add(bnt1)
    balance = client.get_user_balance(message.from_user.id)
    text = f'Ваш баланс: {balance["balance"]}'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(regexp='Перевести')
def transaction(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt1 = telebot.types.KeyboardButton("Меню")
    markup.add(bnt1)
    text = f'Введите адрес кошелька куда хотите перевести: '
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='История')
def history(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt1 = telebot.types.KeyboardButton("Меню")
    markup.add(bnt1)
    transactions = ['1', '2', '3']
    text = f'Ваши транзакции: {transactions}'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Меню' or message.text == "Закрыть админ-панель")
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt1 = telebot.types.KeyboardButton("Кошелек")
    btn2 = telebot.types.KeyboardButton("Перевести")
    btn3 = telebot.types.KeyboardButton("История")
    markup.add(bnt1, btn2, btn3)
    bot.send_message(chat_id=message.chat.id, text='Возвращение в меню', reply_markup=markup)



