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

# Now, you can pass storage to bot.
# States group.
class MyStates(StatesGroup):
    # Just name variables differently  # creating instances of State class is enough from now
    receiver_address = State()
    amount_btc_without_fee = State()
    confirmation = State()


@bot.message_handler(
    func=lambda message: message.text == 'Перевести'
    or message.text == "Создать транзакцию"
)
def start_ex(message):
    user = connection_checker(response=client.get_user_by_tg(message.from_user.id))
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bnt = telebot.types.KeyboardButton("Отмена создания транзакции")
    markup.add(bnt)
    bot.set_state(message.from_user.id, MyStates.receiver_address, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['sender_address'] = message.
    bot.send_message(message.chat.id, text='Введите адрес кошелька куда хотите перевести:', reply_markup=markup)


# Any state
# @bot.message_handler(state="*")
# def any_state(message):
#     """
#     Cancel state
#     """
#     bot.send_message(message.chat.id, "Your state was cancelled.")
#     bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.receiver_address)
def receiver_address(message):
    """
    State 1. Will process when user's state is MyStates.name.
    """
    bot.send_message(message.chat.id, 'Now write me a surname')
    bot.set_state(message.from_user.id, MyStates.amount_btc_without_fee, message.chat.id)



@bot.message_handler(state=MyStates.amount_btc_without_fee)
def amount_btc_without_fee(message):
    """
    State 2. Will process when user's state is MyStates.surname.
    """
    bot.send_message(message.chat.id, "What is your age?")
    bot.set_state(message.from_user.id, MyStates.amount_btc_without_fee, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['receiver_address'] = message.text


# result
@bot.message_handler(state=MyStates.confirmation, is_digit=True)
def ready_for_answer(message):
    """
    State 3. Will process when user's state is MyStates.age.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['amount_btc_without_fee'] = message.text
    bot.set_state(message.from_user.id, MyStates.confirmation, message.chat.id)

# incorrect number
@bot.message_handler(state=MyStates.confirmation, is_digit=False)
def age_incorrect(message):
    """
    Wrong response for MyStates.age
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = ("Ready, take a look:\n<b>"
               f"Sender address: {data['sender_address']}\n"
               f"Receiver address: {data['receiver_address']}\n"
               f"Amount: {data['amount_btc_without_fee']}</b>")
        bot.send_message(message.chat.id, msg, parse_mode="html")
    bot.delete_state(message.from_user.id, message.chat.id)


# register filters