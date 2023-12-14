from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("Kanal qo'shish +"),
            KeyboardButton("Kanal o'chirish -")
        ],
        [
            KeyboardButton('Statistika📊'),
            KeyboardButton("Reklama📈"),
        ],
        [
            KeyboardButton("Adminlar")
        ]
    ],
    resize_keyboard=True
)

ortga = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('🔙Ortga'))

admins = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Admin qo'shish"),
            KeyboardButton("Admin o'chirish -")
        ],
        [
            KeyboardButton('Barcha Adminlar')
        ]
    ],
    resize_keyboard=True)