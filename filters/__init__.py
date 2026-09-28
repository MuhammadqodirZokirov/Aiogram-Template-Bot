from aiogram import Dispatcher

# from .is_admin import AdminFilter


def setup_filters(dp: Dispatcher) -> None:
    # aiogram 3 da filtrlar bind qilinmaydi, to'g'ridan-to'g'ri handlerga beriladi:
    #   @router.message(AdminFilter())
    # Bu yerda global filtrlar qo'shish mumkin:
    #   dp.message.filter(F.chat.type == "private")
    pass
