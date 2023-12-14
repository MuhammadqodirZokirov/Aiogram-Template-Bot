from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"<b>Assalomu alaykum, </b><a href='{message.from_user.url}'>{message.from_user.full_name}</a>!")

    try:
        await db.add_user(user_id=message.from_user.id, join_date=str(message.date)[:-9])
    except:
        pass