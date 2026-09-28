from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.types import Message

router = Router(name="echo")


# Echo bot
@router.message(StateFilter(None))
async def bot_echo(message: Message):
    try:
        # Matn, rasm, stiker va boshqa turdagi xabarlarni ham qaytaradi
        await message.copy_to(chat_id=message.chat.id)
    except TelegramBadRequest:
        await message.answer("Bu turdagi xabarni qaytara olmayman.")
