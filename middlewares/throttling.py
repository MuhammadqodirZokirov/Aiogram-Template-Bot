import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message

DEFAULT_RATE_LIMIT = 0.1


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple antiflood middleware.
    Handler uchun limitni `utils.misc.rate_limit` dekoratori orqali berish mumkin.
    """

    def __init__(self, limit: float = DEFAULT_RATE_LIMIT, key_prefix: str = 'antiflood'):
        self.rate_limit = limit
        self.prefix = key_prefix
        # key -> (oxirgi chaqiruv vaqti, limitdan oshishlar soni)
        self._buckets: dict[str, tuple[float, int]] = {}
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        options = get_flag(data, "throttling") or {}
        limit = options.get("rate", self.rate_limit)
        handler_obj = data.get("handler")
        name = options.get("key") or (handler_obj.callback.__name__ if handler_obj else "message")
        user_id = event.from_user.id if event.from_user else 0
        key = f"{self.prefix}:{name}:{event.chat.id}:{user_id}"

        now = time.monotonic()
        last_call, exceeded = self._buckets.get(key, (0.0, 0))
        if now - last_call < limit:
            exceeded += 1
            self._buckets[key] = (now, exceeded)
            await self.message_throttled(event, exceeded)
            return None

        self._buckets[key] = (now, 0)
        self._cleanup(now)
        return await handler(event, data)

    async def message_throttled(self, message: Message, exceeded_count: int) -> None:
        if exceeded_count <= 2:
            await message.reply("Juda ko'p so'rov! Biroz kuting.")

    def _cleanup(self, now: float, ttl: float = 60.0) -> None:
        # Xotira cheksiz o'smasligi uchun eski yozuvlarni o'chiramiz
        if len(self._buckets) > 10_000:
            self._buckets = {k: v for k, v in self._buckets.items() if now - v[0] < ttl}
