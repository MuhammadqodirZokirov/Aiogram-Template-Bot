from aiogram import Router

from . import echo, help, start

router = Router(name="users")
# echo eng oxirida bo'lishi shart, aks holda boshqa handlerlarni "yutib yuboradi"
router.include_routers(help.router, start.router, echo.router)
