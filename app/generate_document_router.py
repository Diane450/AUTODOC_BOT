from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.zip_or_document_keyboard import zip_or_document_keyboard
from utils.DocumentGenerator import DocumentGenerator
import os
import datetime

generate_document_router = Router()
document_generator = DocumentGenerator()

class DocumentGeneration(StatesGroup):
    template = State()
    user_data_file = State()
    output_type = State()

@generate_document_router.message(Command("generate"))
async def get_user_pattern(message:Message, state:FSMContext):
    await message.answer("Пришли шаблон документа (.docx)")
    await state.set_state(DocumentGeneration.template)


@generate_document_router.message(DocumentGeneration.template, F.document)
async def get_template(message:Message, state:FSMContext, bot:Bot):    
    doc = message.document
    file = await bot.get_file(doc.file_id)
    
    os.makedirs("temp", exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    file_path = f"temp/{timestamp} - {doc.file_name}"
    await bot.download_file(file.file_path, file_path)

    await state.update_data(template=file_path)

    await message.answer("✅ Шаблон получен!\nТеперь пришли Excel (.xlsx) или ссылку на Google Sheets.")
    await state.set_state(DocumentGeneration.user_data_file)


@generate_document_router.message(DocumentGeneration.user_data_file, F.document)
async def get_user_data_file(message:Message, state:FSMContext, bot:Bot):
    doc = message.document
    file = await bot.get_file(doc.file_id)

    os.makedirs("temp", exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    file_path = f"temp/{timestamp} - {doc.file_name}"
    await bot.download_file(file.file_path, file_path)

    await state.update_data(user_data_file=file_path)

    await message.answer("✅ Информация получена!\nВ каком виде вы хотите получить данные:", reply_markup=zip_or_document_keyboard)


@generate_document_router.callback_query(F.data == "output_zip")
async def choose_zip(callback: CallbackQuery, state: FSMContext):
    await state.update_data(output_type="zip")
    await callback.answer("Ваши документы будут присланы в ZIP архиве")

    data = await state.get_data()

    template_path = data["template"]
    user_data_file = data["user_data_file"]
    output_type = data["output_type"]
    file_path = document_generator.generate_document(template_path, user_data_file, output_type)
    await callback.message.answer_document(FSInputFile(file_path))
    document_generator.delete_documents("temp")
    await state.clear()


@generate_document_router.callback_query(F.data == "output_single")
async def choose_single(callback: CallbackQuery, state: FSMContext):
    await state.update_data(output_type="single")
    await callback.answer("Ваши документы будут присланы в едином файле")

    data = await state.get_data()

    template_path = data["template"]
    user_data_file = data["user_data_file"]
    output_type = data["output_type"]
    
    file_path = document_generator.generate_document(template_path, user_data_file, output_type)
    await callback.message.answer_document(FSInputFile(file_path))
    document_generator.delete_documents("temp")
    await state.clear()