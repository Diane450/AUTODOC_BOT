from aiogram import Dispatcher, Bot, types
from app.main_router import main_router
from aiogram.types import BotCommandScopeDefault
import config
import asyncio

bot = Bot(config.TG_TOKEN)

async def main():
    await set_commands()
    dp = Dispatcher()
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