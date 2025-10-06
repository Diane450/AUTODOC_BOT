from aiogram import BaseMiddleware
from utils.Logger import logger

class UserInfoMiddleware(BaseMiddleware):
    """Добавляет информацию о пользователе в data каждого хэндлера."""

    async def __call__(self, handler, event, data):
        user = getattr(event, "from_user", None)
        if not user and hasattr(event, "message"):
            user = getattr(event.message, "from_user", None)

        if user:
            data["user_id"] = user.id
            data["username"] = user.username
        else:
            data["user_id"] = None
            data["username"] = None
        return await handler(event, data)