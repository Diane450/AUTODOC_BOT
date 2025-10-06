from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Awaitable, Any, Dict
from utils.Logger import logger
import config


class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            user_id = getattr(getattr(event, "from_user", None), "id", "unknown")
            logger.exception(f"Error validating user input {user_id}: {e}")

            if isinstance(event, Message):
                await event.answer(config.ERROR_USER_MESSAGE)
            elif isinstance(event, CallbackQuery):
                await event.message.answer(config.ERROR_USER_MESSAGE)
            return None
