import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards.default.Admins_default_keyboards import admin

from data import config
from filters import IsBotAdmin
from keyboards.keyboard_create_function import cik
from loader import dp, bot, db


@dp.message_handler(IsBotAdmin(), Text("Kanal qo'shish +"))
async def addchanel(message: types.Message, state: FSMContext):
    await message.answer(text=f"1. Birinchi bo'lib botni @{config.BOT_NAME} ni kanalingizda administrator qiling.\n\n"
                              "2. Administrator qilganingizdan keyn esa kanalingizni Public link\n"
                              "(@channel)manzilini yoki kanal ID raqamini yuboring (-10012334465) yoki \n"
                              "kanalingizdan biron bir matnli postni Forward from formatida yuboring")
    await state.set_state("add_chanel")


@dp.message_handler(IsBotAdmin(), state="add_chanel", content_types=types.ContentTypes.ANY)
async def add_channel(message: types.Message, state: FSMContext):
    await state.finish()
    qosh = True
    try:
        chat_id = message.forward_from_chat.id
    except:
        chat_id = message.text
    try:
        chanel = await bot.get_chat(chat_id)
        chat_title = chanel["title"]
        chat_url = chanel['invite_link']
        chat_id = chanel['id']
    except:
        qosh *= False
    if qosh:
        try:
            await db.add_channel(channel_id=str(chat_id), link=chat_url)
            await message.answer(text=f"✅ <a href='{chat_url}'>{chat_title}</a>\n"
                                      f"Kanali qo'shildi", disable_web_page_preview=True)
        except asyncpg.exceptions.UniqueViolationError:
            await message.answer("❌Bu kanal avvaldan qo'shilgan")
    else:
        await message.answer("Nimadir xato ketdi!\n"
                             "Koʻp uchraydigan xatolar:\n\n"
                             "*Kanalda bot administrator ekanligini tekshiring.\n"
                             "*Kanalda siz administrator emassiz.\n"
                             "*Kanal manzili/ID si notoʻgʻri yozilgan\n"
                             "\n"
                             "agar xato ketmasa texnik yordamga yozing:\n"
                             "@ZokirovMuhammadqodir")


@dp.message_handler(IsBotAdmin(), text="Kanal o'chirish -")
async def remove_channel(message: types.Message, state: FSMContext):
    await state.finish()
    channels = await db.select_all_channels()
    if len(channels) == 0:
        await message.answer(text="❌Sizda hali kanallar mavjud emas❗\n"
                                  "Kanal qo'shib qayta urunib ko'ring❗")
    else:
        kanallar = {}
        for kanal in await db.select_all_channels():
            chanell = await bot.get_chat(kanal[0])
            chanel_title = chanell['title']
            kanallar[chanel_title] = f"rm_channel:{kanal[0]}"
        rm_channels = cik(keyboards=kanallar, ortga_btn=True)
        await message.answer(text="O'chirib tashlamoqchi bo'lgan kanalni tanlang", reply_markup=rm_channels)
        await state.set_state('rm_channel')


@dp.callback_query_handler(state='rm_channel')
async def remove_cahnnels(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    data = call.data
    if data.startswith("rm_channel:"):
        channel_id = data[11:]
        await db.delete_channel(channel_id=channel_id)
        await call.message.edit_text("✅Kanal o'chirib tashlandi")

    elif data.startswith('cancel'):
        await state.finish()
        await call.message.answer(
            f"<b>Assalomu alaykum, </b> <a href='{call.message.from_user.url}'>{call.message.from_user.full_name}</a>\n"
            f"<b>Admin panelga hush kelibsiz</b>", reply_markup=admin)
