from aiogram import Dispatcher, Bot, types
from app.main_router import main_router
from app.generate_document_router import generate_document_router
from aiogram.types import BotCommandScopeDefault
from middlewares.ErrorHandlerMiddleware import ErrorHandlerMiddleware
from middlewares.UserInfoMiddleware import UserInfoMiddleware
from aiogram.exceptions import TelegramNetworkError
from utils.CleanUpUtils import clean_old_temp_files
from utils.Logger import logger
import asyncio
import os

bot = Bot("7460551340:AAEG0NNuf_KiScgjuYOInEN34jCJ34zHr9k")
dp = Dispatcher()

async def main():
    
    await set_commands()
    setup_bot()
    await start_bot()


async def set_commands():
    commands = [
        types.BotCommand(command="start", description="Запуск бота"),
        types.BotCommand(command="help", description="Помощь"),
        types.BotCommand(command="generate", description="Сгенерировать документы")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


def setup_bot():
    dp.update.middleware(ErrorHandlerMiddleware())
    dp.update.middleware(UserInfoMiddleware())
    main_router.include_router(generate_document_router)
    dp.include_router(main_router)
    asyncio.create_task(clean_old_temp_files())


async def start_bot():
    retry_delay = 5

    while True:
        try:
            logger.info("🚀 Start bot...")
            await dp.start_polling(bot)
            retry_delay(5)
        except TelegramNetworkError as e:
            logger.error(f"⚠️ Network error: {e}. Retry in {retry_delay} sec...")
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 300)  # увеличиваем задержку до 5 минут макс
        except Exception as e:
            logger.exception(f"❌ Unknown error: {e}. Retry in {retry_delay} sec...")
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 300)


if __name__ == "__main__":
    asyncio.run(main())