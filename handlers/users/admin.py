import aiogram.utils.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from data import config
from filters import IsBotAdmin
from keyboards.keyboard_create_function import cik
from keyboards.default.Admins_default_keyboards import admin
from loader import dp, bot, db


@dp.message_handler(IsBotAdmin(), commands='admin')
async def admin_panel(message: types.Message):
    await message.answer(
        f"<b>Assalomu alaykum, </b> <a href='{message.from_user.url}'>{message.from_user.full_name}</a> <b>Admin panelga hush kelibsiz</b>",
        reply_markup=admin)


@dp.message_handler(IsBotAdmin(), text='Adminlar')
async def Adminlar_list(message: types.Message, state: FSMContext):
    global inline_admins_list
    inline_admins_list = InlineKeyboardMarkup(row_width=1)
    for admin in await db.select_all_admins():
        user = await bot.get_chat(admin['admin_id'])
        fullname = user.full_name
        inline_admins_list.add(
            InlineKeyboardButton(text=fullname, callback_data=f"delete_admin_id:{admin['admin_id']}"))

    inline_admins_list.add(InlineKeyboardButton("Admin qo'shish", callback_data="add_admin"))
    inline_admins_list.add(InlineKeyboardButton(text="🔙Ortga", callback_data="cancel"))

    await message.answer("Adminlar ro'yhati", reply_markup=inline_admins_list)
    a = await message.answer(text="Bajarilmoqda...", reply_markup=ReplyKeyboardRemove())
    await a.delete()
    await state.set_state("add_remove")


@dp.callback_query_handler(IsBotAdmin(), state="add_remove")
async def Admin_add(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    call_data = call.data
    if call_data == 'add_admin':
        await call.message.answer("Admin qo'shish uchun\n"
                                  "Foydalanuvchi ID botga yuboring..")
        await state.set_state("add_admin")
    elif call_data.startswith('delete_admin_id:'):
        id = call_data[16:]
        user = await bot.get_chat(call_data[16:])
        fullname = user.full_name
        delete_confirm = cik(keyboards={"Ha chetlatilsin": f'confirm_rm_admin:{id}'}, ortga_btn=True)
        await call.message.answer("Admin\n"
                                  f"ID: {id}\n"
                                  f"Ismi: {fullname}\n", reply_markup=delete_confirm)
        await state.set_state("confirm_rm")

    elif call_data == 'cancel':
        await call.message.answer(
            f"<b>Assalomu alaykum, </b> <a href='{call.message.from_user.url}'>{call.message.from_user.full_name}</a> <b>Admin panelga hush kelibsiz</b>",
            reply_markup=admin)
        await state.finish()


@dp.message_handler(IsBotAdmin(), state="add_admin")
async def answer_admin_add(message: types.Message, state: FSMContext):
    tasdiqlash = cik(keyboards={"Admin sifatida tayinlash": 'admin_qilish'}, ortga_btn=True)
    try:
        if message.is_forward():
            chat_id = message.forward_from.id
            user = await bot.get_chat(chat_id)
            name = user.full_name
            username = user.username

            if username:
                user_id = user.id
                await message.answer(text=f"Ismi: {name}\n"
                                          f"ID: {user_id}\n"
                                          f"Foydanaluvchi nomi: @{username}\n", reply_markup=tasdiqlash)
                await state.update_data({
                    'user_id': user_id,
                    'name': name,
                    'username': username
                })
            else:
                user_id = user.id
                await message.answer(text=f"Ismi: {name}\n"
                                          f"ID: {user_id}\n", reply_markup=tasdiqlash)
                await state.update_data({
                    'user_id': user_id,
                    'name': name,
                })
        elif message.content_type == 'text':
            chat_id = message.text
            user = await bot.get_chat(chat_id)
            name = user.full_name
            username = user.username
            if username:
                user_id = user.id
                await message.answer(text=f"Ismi: {name}\n"
                                          f"ID: {user_id}\n"
                                          f"Foydanaluvchi nomi: @{username}\n", reply_markup=tasdiqlash)
                await state.update_data({
                    'user_id': user_id,
                    'name': name,
                    'username': username
                })
            else:
                user_id = user.id
                await message.answer(text=f"Ismi: {name}\n"
                                          f"ID: {user_id}\n", reply_markup=tasdiqlash)
                await state.update_data({
                    'user_id': user_id,
                    'name': name,
                })
        else:
            await message.answer('Uzr qandaydir xato ketdi.')
            await state.finish()
    except aiogram.utils.exceptions.ChatNotFound:
        await message.answer("Bunday ID mavjud emas!!!")
        await state.finish()

    await state.set_state('confirm')


@dp.callback_query_handler(IsBotAdmin(), text="admin_qilish", state="confirm")
async def new_admin_confirm(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    user = await bot.get_chat(user_id)
    name = user.full_name
    admin_id = str(user_id)
    await db.add_admin(admin_id)
    await call.message.delete()
    await call.message.answer(f"<a href='{user.user_url}'>{name}</a> muvaffaqiyatli tarzda Admin qilib tayinlandi.",
                              reply_markup=admin)
    try:

        await bot.send_message(chat_id=user_id, text=f"Xurmatli {name}\n"
                                                     f"siz quyidagi botni admini etib tayinlandingiz\n"
                                                     f"@{config.BOT_NAME}\n")
    except:
        pass
    await state.finish()  # complete


@dp.callback_query_handler(IsBotAdmin(), Text(startswith='confirm_rm_admin:'), state='confirm_rm')
async def remove_admin_confirm(call: types.CallbackQuery, state: FSMContext):
    inline_admins_list = InlineKeyboardMarkup(row_width=1)
    call_data = call.data
    if call_data == 'cancel':
        await call.message.answer(f"Adminlar:",
                                  reply_markup=inline_admins_list)
        await state.finish()
    elif call_data.startswith('confirm_rm_admin'):
        user = await bot.get_chat(call_data[17:])
        name = user.full_name
        admin_id = str(user.id)
        await db.remove_admin(admin_id=admin_id)
        await call.answer("Admin muvaffaqiyatli chetlatildi", show_alert=True)
        await call.message.edit_text(f"<a href='{user.user_url}'>{name}</a> Admin muvaffaqiyatli chetlatildi")
        await call.message.answer(
            f"<b>Assalomu alaykum, </b> <a href='{call.message.from_user.url}'>{call.message.from_user.full_name}</a> <b>Admin panelga hush kelibsiz</b>",
            reply_markup=admin)

        try:

            await bot.send_message(chat_id=user.id, text=f"Xurmatli {name}\n"
                                                         f"siz quyidagi botni adminlikdan chetlatildingiz.\n"
                                                         f"@{config.BOT_NAME}\n")
        except:
            pass
        await state.finish()