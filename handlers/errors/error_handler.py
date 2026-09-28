import logging

from aiogram import Router
from aiogram.exceptions import (
    TelegramAPIError,
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramRetryAfter,
    TelegramUnauthorizedError,
)
from aiogram.types import ErrorEvent

router = Router(name="errors")


@router.error()
async def errors_handler(event: ErrorEvent):
    """
    Exceptions handler. Barcha routerlardagi xatolarni ushlaydi.
    :param event: ErrorEvent (event.update, event.exception)
    :return: stdout logging
    """
    exception = event.exception
    update = event.update

    if isinstance(exception, TelegramUnauthorizedError):
        logging.error(f'Unauthorized (token noto\'g\'ri): {exception}')
    elif isinstance(exception, TelegramForbiddenError):
        # Foydalanuvchi botni bloklagan va h.k.
        logging.warning(f'Forbidden: {exception}')
    elif isinstance(exception, TelegramRetryAfter):
        logging.warning(f'RetryAfter {exception.retry_after}s: {exception} (update_id={update.update_id})')
    elif isinstance(exception, TelegramBadRequest):
        # MessageNotModified, MessageToDeleteNotFound, CantParseEntities va h.k.
        logging.warning(f'BadRequest: {exception} (update_id={update.update_id})')
    elif isinstance(exception, TelegramAPIError):
        logging.error(f'TelegramAPIError: {exception} (update_id={update.update_id})')
    else:
        logging.error(f"update_id={update.update_id}: {exception}", exc_info=exception)

    return True
