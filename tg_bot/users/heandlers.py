import telebot
from tg_bot.start_bot import bot


@bot.message_handler(commands=["start"])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt1 = telebot.types.KeyboardButton("Кошелек")
    btn2 = telebot.types.KeyboardButton("Перевести")
    btn3 = telebot.types.KeyboardButton("История")
    markup.add(bnt1, btn2, btn3)
    text = f'Привет, {message.from_user.full_name}, я крипто-кошелёк!\n' \
            f'ты можешь хранить и отправлять криптовалюту'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(regexp='Кошелек')
def wallet(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt1 = telebot.types.KeyboardButton("Меню")
    markup.add(bnt1)
    balance = 0
    text = f'Ваш баланс: {balance}'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(regexp='Перевести')
def wallet(message):
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


@bot.message_handler(regexp='Меню')
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt1 = telebot.types.KeyboardButton("Кошелек")
    btn2 = telebot.types.KeyboardButton("Перевести")
    btn3 = telebot.types.KeyboardButton("История")
    markup.add(bnt1, btn2, btn3)
    bot.send_message(chat_id=message.chat.id, text='Возвращение в меню', reply_markup=markup)



