from aiogram import Dispatcher, Bot, types
from app.main_router import main_router
from app.generate_document_router import generate_document_router
from aiogram.types import BotCommandScopeDefault
import config
import asyncio
from middlewares.ErrorHandlerMiddleware import ErrorHandlerMiddleware
from middlewares.UserInfoMiddleware import UserInfoMiddleware

bot = Bot(config.TG_TOKEN)

async def main():
    await set_commands()
    dp = Dispatcher()
    dp.update.middleware(ErrorHandlerMiddleware())
    dp.update.middleware(UserInfoMiddleware())
    main_router.include_router(generate_document_router)
    dp.include_router(main_router)
    await dp.start_polling(bot)

async def set_commands():
    commands = [
        types.BotCommand(command="start", description="Запуск бота"),
        types.BotCommand(command="help", description="Помощь"),
        types.BotCommand(command="generate", description="Сгенерировать документы")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

if __name__ == "__main__":
    asyncio.run(main())