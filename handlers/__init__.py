from aiogram import Router

from . import channels, errors, groups, users


def setup_routers() -> Router:
    router = Router(name="root")
    # Tartib muhim: users ichidagi echo eng oxirida turadi
    router.include_routers(
        errors.router,
        groups.router,
        channels.router,
        users.router,
    )
    return router
