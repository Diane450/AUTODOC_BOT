from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import os
import datetime

generate_document_router = Router()

class DocumentGeneration(StatesGroup):
    pattern = State()
    data = State()

@generate_document_router.message(Command("generate"))
async def get_user_pattern(message:Message, state:FSMContext):
    await message.answer("Пришли шаблон документа (.docx)")
    await state.set_state(DocumentGeneration.pattern)


@generate_document_router.message(DocumentGeneration.pattern, F.document)
async def get_pattern(message:Message, state:FSMContext, bot:Bot):    
    doc = message.document
    file = await bot.get_file(doc.file_id)
    
    os.makedirs("temp", exist_ok=True)

    file_path = f"temp/{doc.file_name}-{datetime.datetime.now()}"
    await bot.download_file(file.file_path, file_path)

    await state.update_data(pattern=file_path)

    await message.answer("✅ Шаблон получен!\nТеперь пришли Excel (.xlsx) или ссылку на Google Sheets.")
    await state.set_state(DocumentGeneration.data)

