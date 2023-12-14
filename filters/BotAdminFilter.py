from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db


class IsBotAdmin(BoundFilter):
    async def check(self, message: types.Message):
        admin_id = [admin for admins in await db.select_all_admins() for admin in admins]
        return str(message.from_user.id) in admin_id