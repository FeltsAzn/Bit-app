from telebot import TeleBot, StateMemoryStorage, custom_filters
from tg_bot.config import BOT_TOKEN


state_storage = StateMemoryStorage()
bot = TeleBot(BOT_TOKEN, state_storage=state_storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
