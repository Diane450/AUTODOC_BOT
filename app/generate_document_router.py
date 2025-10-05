from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.zip_or_document_keyboard import zip_or_document_keyboard
from utils.DocumentUtils import DocumentUtils
from urllib.parse import urlparse
from utils.DirectoryUtils import DirectoryUtils
from utils.ValidateUtils import ValidateUtils
from utils.BotUtils import BotUtils


generate_document_router = Router()
document_utils = DocumentUtils()
directory_utils = DirectoryUtils()
validate_utils = ValidateUtils()
bot_utils = BotUtils()

class DocumentGeneration(StatesGroup):
    template_path = State()
    user_data_file_path = State()
    output_type = State()

@generate_document_router.message(Command("generate"))
async def get_user_pattern(message:Message, state:FSMContext):
    await message.answer("Пришли шаблон документа (.docx)")
    await state.set_state(DocumentGeneration.template_path)
    directory_utils.create_folder()


@generate_document_router.message(DocumentGeneration.template_path, F.document)
async def get_template_path(message:Message, state:FSMContext, bot:Bot):    
    doc = message.document

    temp_file_path = await document_utils.download_file(bot, doc)

    await state.update_data(template_path=temp_file_path)
    await message.answer("✅ Шаблон получен!\nТеперь пришли Excel (.xlsx) или ссылку на Google Sheets.")
    await state.set_state(DocumentGeneration.user_data_file_path)


@generate_document_router.message(DocumentGeneration.user_data_file_path, F.document)
async def get_user_data_file_path_doc(message: Message, state: FSMContext, bot:Bot):
    doc = message.document

    temp_file_path = await document_utils.download_file(bot, doc)

    await state.update_data(user_data_file_path=temp_file_path)
    await message.answer("✅ Данные (Excel) получены!\nВ каком виде прислать результат?", reply_markup=zip_or_document_keyboard)


@generate_document_router.message(DocumentGeneration.user_data_file_path, F.text)
async def get_user_data_file_path_link(message: Message, state: FSMContext):
    text = message.text.strip()

    if not validate_utils.looks_like_gsheets(text):
        await message.answer("Поддерживаемые ссылки: Google Sheets (docs.google.com/spreadsheets/...) или прямая ссылка на .xlsx.")
        return

    await state.update_data(user_data_file_path=text)
    await message.answer("✅ Ссылка принята!\nВ каком виде прислать результат?", reply_markup=zip_or_document_keyboard)


@generate_document_router.callback_query(F.data.in_(["output_zip", "output_single"]))
async def choose_zip(callback: CallbackQuery, state: FSMContext):
    
    output_type = callback.data.removeprefix("output_")
    await state.update_data(output_type=output_type)

    text = bot_utils.get_text_for_output_type(output_type)
    await callback.answer(text)

    data = await state.get_data()

    template_path = data["template_path"]
    user_data_file_path = data["user_data_file_path"]

    file_path = document_utils.generate_document(template_path,user_data_file_path, output_type)
    
    await callback.message.answer_document(FSInputFile(file_path))
    
    directory_utils.remove_temp_files()
    await state.clear()