from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from loader import dp, db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


programmer = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Dasturchi", url="https://t.me/MuhammadqodirZokirovPortfolio")],
    ]
)
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Bog'lanish 📱\n\n",
            "Telegram: @ZokirovMuhammadqodir\n",
            "Telephone: +998337470926\n"
            "\nSiznig botimiz haqidagi talab va takliflaringizni 24/7 holatda ko'rib chiqamiz")

    await message.answer("".join(text), reply_markup=programmer)

@dp.message_handler(commands='profile')
async def bot_profile(message: types.Message):
    user_data = await db.select_user(user_id=str(message.from_user.id))
    join_date = user_data[2]
    await message.answer(f"<b>Name: {message.from_user.full_name}\n"
                         f"User id: <code>{message.from_user.id}</code>\n"
                         f"Join date: {join_date}\n"
                         f"<i>{str(message.date)[:-9]}</i></b>")
