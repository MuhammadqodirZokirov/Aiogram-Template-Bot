from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    dp.message.middleware(ThrottlingMiddleware())
