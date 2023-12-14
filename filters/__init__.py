from aiogram import Dispatcher

from loader import dp
from .BotAdminFilter import IsBotAdmin

if __name__ == "filters":
    dp.filters_factory.bind(IsBotAdmin)