from aiogram import F, Router

router = Router(name="groups")
router.message.filter(F.chat.type.in_({"group", "supergroup"}))
