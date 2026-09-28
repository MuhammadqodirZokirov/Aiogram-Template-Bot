from aiogram import flags


def rate_limit(limit: float, key: str | None = None):
    """
    Handler uchun rate limit va key ni belgilovchi dekorator.
    Router dekoratoridan PASTDA yozilishi kerak:

        @router.message(Command("test"))
        @rate_limit(5, "test")
        async def handler(message: Message): ...

    :param limit: sekundlarda limit
    :param key: throttling kaliti (default: handler nomi)
    """
    options = {"rate": limit}
    if key:
        options["key"] = key
    return flags.throttling(options)
