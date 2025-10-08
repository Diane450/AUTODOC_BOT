from aiogram import Dispatcher, Bot, types
from app.main_router import main_router
from app.generate_document_router import generate_document_router
from aiogram.types import BotCommandScopeDefault
from middlewares.ErrorHandlerMiddleware import ErrorHandlerMiddleware
from middlewares.UserInfoMiddleware import UserInfoMiddleware
from utils.CleanUpUtils import clean_old_temp_files
import config
import asyncio
import os

bot = Bot(os.environ["TG_TOKEN"])

async def main():
    await set_commands()
    dp = Dispatcher()
    dp.update.middleware(ErrorHandlerMiddleware())
    dp.update.middleware(UserInfoMiddleware())
    main_router.include_router(generate_document_router)
    dp.include_router(main_router)
    asyncio.create_task(clean_old_temp_files())
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