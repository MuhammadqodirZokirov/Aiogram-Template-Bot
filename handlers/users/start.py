from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router(name="start")


@router.message(CommandStart())
async def bot_start(message: Message):
    await message.answer(f"Salom, {html.quote(message.from_user.full_name)}!")
