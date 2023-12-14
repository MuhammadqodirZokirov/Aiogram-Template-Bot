from aiogram import types

from filters import IsBotAdmin
from loader import db, dp


@dp.message_handler(IsBotAdmin(), text="Statistika📊")
async def bot_statistika(message: types.Message):
    nimadir = await message.answer("⏳")
    n = await db.count_users()
    today_users = 0
    active_users = 0
    users = await db.select_all_users()
    for user in users:
        today = str(message.date)[:-9]
        if today == user['join_date']:
            today_users += 1
        if user['status'] == 'active':
            active_users += 1

    await nimadir.edit_text(f"<b>Statistika📊\n\n"
                         f"👤Foydalanuvchilar: {n}\n\n"
                         f"✅Faol foydalanuvchilar: {active_users}\n"
                         f"🚫Faol bo'lmagan foydalanuvchilar: {int(n)-active_users}\n\n"
                         f"Bugun qo'shilgan foydalanuvchilar: {today_users}\n\n"
                         f"📅 Sana : {str(message.date)[:-9]}</b>")