from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ortga = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton('🔙Ortga', callback_data='🔙Ortga'))

inline_admins = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Admin qo'shish", callback_data="add_admin"),
            InlineKeyboardButton("Admin o'chirish", callback_data="rm_admin")
        ],
        [
            InlineKeyboardButton('Barcha Adminlar', callback_data="all_admins")
        ],
        [
            InlineKeyboardButton('🔙Ortga', callback_data='🔙Ortga')
        ]
    ],
    resize_keyboard=True
)