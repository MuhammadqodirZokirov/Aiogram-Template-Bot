from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


def ortga_btn():
    btn = InlineKeyboardMarkup()
    btn.insert(InlineKeyboardButton(text="🔙 Ortga", callback_data="cancel"))
    return btn


def cik(keyboards: dict, row_width: int = 1, ortga_btn: bool = False, callback_object_name: CallbackData = None):
    inkb = InlineKeyboardMarkup()
    inkb.row_width = row_width
    if callback_object_name:
        for text, callback_data in keyboards.items():
            inkb.insert(
                InlineKeyboardButton(text=text, callback_data=callback_object_name.new(item_name=callback_data)))
        if ortga_btn == True:
            inkb.insert(InlineKeyboardButton(text="🔙 Ortga", callback_data="cancel"))
        return inkb
    elif callback_object_name == None:
        for text, callback_data in keyboards.items():
            inkb.insert(InlineKeyboardButton(text=text, callback_data=callback_data))
        if ortga_btn == True:
            inkb.insert(InlineKeyboardButton(text="🔙 Ortga", callback_data="cancel"))
        return inkb


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def cdk(keyboards: any, row_witdh: int = 1, ortga_btn: bool = False, resize_keyboad: bool = True):
    keyb = ReplyKeyboardMarkup()
    keyb.resize_keyboard = resize_keyboad
    keyb.row_witdh = row_witdh
    for text in keyboards:
        keyb.insert(KeyboardButton(f'{text}'))
    if ortga_btn:
        keyb.insert(KeyboardButton('🔙 Ortga'))

    return keyb
