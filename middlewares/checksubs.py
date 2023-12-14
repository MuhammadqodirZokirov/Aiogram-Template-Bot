from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db, bot
from utils.misc import subscription


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
            text = update.message.text
            try:
                if text.startswith("/start"):
                    return
                if text.startswith("/help"):
                    return
            except:
                return
        elif update.callback_query:
            user = update.callback_query.from_user.id
            return
        else:
            return
        result = "<b>Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:</b>\n"
        final_status = True
        btn = InlineKeyboardMarkup(row_width=1)
        for channel in await db.select_all_channels():
            status = await subscription.check(user_id=user,
                                              channel=channel[0])
            final_status *= status
            if not status:
                chanel = await bot.get_chat(channel[0])
                chat_title = chanel["title"]
                invite_link = channel[1]
                btn.add(InlineKeyboardButton(text=f"{chat_title}", url=invite_link))
        btn.add(InlineKeyboardButton(text="Tasdiqlash ✅", callback_data="check"))

        if not final_status:
            await update.message.answer(result, reply_markup=btn, disable_web_page_preview=True)
            raise CancelHandler()