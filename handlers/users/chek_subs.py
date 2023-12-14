from aiogram import types


from loader import dp, bot, db


async def check_sub_channels(channels, user_id):
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[0], user_id=user_id)
        if chat_member['status'] == 'left':
            return False
    return True


@dp.callback_query_handler(text="check")
async def check_subs(call: types.CallbackQuery):
    user_id = call.from_user.id
    if await check_sub_channels(channels=await db.select_all_channels(), user_id=user_id):
        await call.message.delete()
        await bot.send_message(user_id, f"{call.from_user.full_name} <b>Quyidagi menulardan birini tanlang</b>")
    else:
        await call.answer("❌Homiy kanalimizga ulanmaganga o'xshaysiz\n"
                          "Ulanib qayta  Tasdiqlash ✅ tugmasini bosing❗️", show_alert=True)
