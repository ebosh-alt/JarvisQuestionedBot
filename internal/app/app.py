from aiogram import Dispatcher, Bot

from config import Config

config = Config.load()

dp = Dispatcher()
bot = Bot(config.telegram.bot_token)
