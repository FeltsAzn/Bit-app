import telebot
from http.client import HTTPException
from tg_bot.start_bot import bot


def connection_checker(response):
    if 'db_error' in response.keys():
        raise ConnectionError(f"{response['db_error']}")
    elif "not_found" in response.keys():
        raise AttributeError(f"{response['not_found']}")
    elif "db_data_error" in response.keys():
        raise ValueError(f"{response['db_data_error']}")
    elif "server_error" in response.keys():
        raise HTTPException(f"{response['server_error']}")
    else:
        return response


def exception_info(message, http_mark_text, conn_mark_text, exception):
    if isinstance(exception, HTTPException):
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton(http_mark_text)
        markup.add(bnt)
        text = f'Ой, что-то пошло не так :(\n' \
               f'Возможно сервер не отвечает.\n' \
               f'Попробуйте повторить позже.'
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
    elif isinstance(exception, ConnectionError):
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        bnt = telebot.types.KeyboardButton(conn_mark_text)
        markup.add(bnt)
        text = f'Ой, что-то пошло не так :(\n' \
               f'Попробуйте обратиться позже.'
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)