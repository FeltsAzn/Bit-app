from tg_bot.loader import bot
from tg_bot import admin
from tg_bot import users


def start():
    bot.infinity_polling(skip_pending=True)


if __name__ == '__main__':
    try:
        start()
    except Exception as ex:
        with open("tg_bot/logs.txt", 'a') as file:
            file.write(f'{ex}\n')
        start()
