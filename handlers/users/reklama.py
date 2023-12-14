import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsBotAdmin
from keyboards.default.Admins_default_keyboards import ortga, admin
from loader import db, bot, dp

@dp.message_handler(IsBotAdmin(), text="Reklama📈")
async def bot_REK(message: types.Message, state: FSMContext):
    await message.answer(f'Reklamani jo\'nating', reply_markup=ortga)
    await state.set_state('rek')

@dp.message_handler(IsBotAdmin(), content_types=types.ContentType.ANY, state='rek')
async def bot_REK(message: types.Message, state: FSMContext):
    if message.text == "🔙Ortga":
        await state.reset_state(False)
        await message.answer(f'Bosh menu', reply_markup=admin)
    else:
        unactive_user = 0
        active_user = 0
        users = await db.count_users()
        time = int(users)*0.005
        soat = time // 3600
        minut = (time % 3600) // 60
        second = (time % 3600) // 60
        await message.answer("Foydalanuvchilarga xabar yuborish boshlandi\n"
                             f"Xabar yuborish taxminiy vaqti🕒 <code>{soat}:{minut}:{second} </code>", reply_markup=ortga)
        for ret in await db.select_all_users():
            try:
                if message.reply_markup:
                    await bot.copy_message(
                        chat_id=ret[0],
                        from_chat_id=message.from_user.id,
                        message_id=message.message_id, reply_markup=message.reply_markup)
                else:
                    await bot.copy_message(
                        chat_id=ret[0],
                        from_chat_id=message.from_user.id,
                        message_id=message.message_id, )
                await db.update_status(status='active', user_id=ret[0])
                active_user += 1
                await asyncio.sleep(0.05)
            except:
                unactive_user += 1
                await db.update_status(status='unactive', user_id=ret[0])
        text = "✅ Post barcha aktiv foydalanuvchilarga yuborildi.\n\n"
        text += f"Barcha foydalanuvchilar: {active_user + unactive_user} ta\n"
        text += f"Aktiv foydalanuvchilar: {active_user} ta \n"
        text += f"Aktiv bo'lmagan foydalanuvchilar: {unactive_user} ta"
        await message.answer(text=text, reply_markup=ortga)