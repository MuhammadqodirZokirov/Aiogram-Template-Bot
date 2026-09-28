import asyncio
import logging

from aiogram import Bot

import utils  # noqa: F401  (logging sozlamalari)
from filters import setup_filters
from handlers import setup_routers
from loader import bot, dp
from middlewares import setup_middlewares
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(bot: Bot):
    # Birlamchi komandalar (/start va /help)
    await set_default_commands(bot)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(bot)


async def main():
    setup_middlewares(dp)
    setup_filters(dp)
    dp.include_router(setup_routers())
    dp.startup.register(on_startup)

    # Webhook o'rnatilgan bo'lsa, polling ishlamaydi
    await bot.delete_webhook()
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi")
