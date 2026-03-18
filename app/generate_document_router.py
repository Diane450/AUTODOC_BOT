from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.zip_or_document_keyboard import zip_or_document_keyboard
from utils.OuputUtils import OutputUtils
from utils.DirectoryUtils import DirectoryUtils
from utils.ValidateUtils import ValidateUtils
from utils.BotUtils import BotUtils
from utils.Logger import logger 
import os


generate_document_router = Router()
document_utils = OutputUtils()
directory_utils = DirectoryUtils()
validate_utils = ValidateUtils()
bot_utils = BotUtils()

class DocumentGeneration(StatesGroup):
    template_path = State()
    user_data_file_path = State()
    output_type = State()


@generate_document_router.message(Command("generate"))
async def get_user_pattern(message:Message, state:FSMContext):
    await message.answer("Пришлите шаблон документа (.docx)")
    await state.set_state(DocumentGeneration.template_path)
    directory_utils.create_folder()


@generate_document_router.message(DocumentGeneration.template_path, F.document)
async def get_template_path(message:Message, state:FSMContext, bot:Bot, user_id: int = None, username: str = None):
    doc = message.document
    
    if not validate_utils.is_docx(doc):
        await message.answer("❌Вы отправили некорректный шаблон. Отправьте шаблон в формате docx❌")
        logger.warning(f"User {user_id} ({username}) sent incorrect template")
    else:
        temp_file_path = await bot_utils.download_file(bot, doc)
        is_valid, error_message = validate_utils.check_template_syntax(temp_file_path)
        if not is_valid:
            await message.answer(error_message, parse_mode="HTML")
            logger.warning(f"User {user_id} ({username}) sent template with syntax error")
            
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            return
        
        await state.update_data(template_path=temp_file_path)
        await message.answer("✅ Шаблон получен!\nТеперь пришли Excel (.xlsx) или ссылку на Google Sheets.")
        await state.set_state(DocumentGeneration.user_data_file_path)
        logger.info(f"Got user {user_id} ({username}) template")


@generate_document_router.message(DocumentGeneration.user_data_file_path, F.document)
async def get_user_data_file_path_doc(message: Message, state: FSMContext, bot:Bot, user_id: int = None, username: str = None):
    doc = message.document

    temp_file_path = await bot_utils.download_file(bot, doc)

    await state.update_data(user_data_file_path=temp_file_path)
    await message.answer("✅ Данные (Excel) получены!\nВ каком виде прислать результат?", reply_markup=zip_or_document_keyboard)
    logger.info(f"Got user {user_id} ({username}) template")


@generate_document_router.message(DocumentGeneration.user_data_file_path, F.text)
async def get_user_data_file_path_link(message: Message, state: FSMContext, user_id: int = None, username: str = None):
    text = message.text.strip()

    if not validate_utils.looks_like_gsheets(text):
        await message.answer("⚠️Поддерживаемые ссылки: Google Sheets (docs.google.com/spreadsheets/...) или прямая ссылка на .xlsx.⚠️")
        logger.warning(f"User {user_id} ({username}) sent incorrect data file")
        return

    await state.update_data(user_data_file_path=text)
    await message.answer("✅ Ссылка принята!\nВ каком виде прислать результат?", reply_markup=zip_or_document_keyboard)
    logger.info(f"Got user {user_id} ({username}) data file")


@generate_document_router.callback_query(F.data.in_(["output_zip", "output_single", "output_both"]))
async def choose_zip(callback: CallbackQuery, state: FSMContext, user_id: int = None, username: str = None):
    
    output_type = callback.data.removeprefix("output_")
    logger.info(f"user {user_id} ({username}) has selected output_type: {output_type}")
    await state.update_data(output_type=output_type)

    text = bot_utils.get_text_for_output_type(output_type)
    await callback.answer(text)

    await callback.message.edit_reply_markup(reply_markup=None)
    wait_msg = await callback.message.answer("⏳ Генерирую документы, пожалуйста, подождите...")

    data = await state.get_data()

    if not data or "template_path" not in data or "user_data_file_path" not in data:
        await wait_msg.delete()
        await callback.message.answer("⚠️ Сессия устарела. Начните заново: /generate")
        return

    template_path = data["template_path"]
    user_data_file_path = data["user_data_file_path"]

    files_to_remove = [template_path, user_data_file_path]

    try:
        if output_type == "both":
            file_path_zip = document_utils.generate_output(template_path, user_data_file_path, "zip")
            file_path_single = document_utils.generate_output(template_path, user_data_file_path, "single")
            
            await callback.message.answer_document(FSInputFile(file_path_zip))
            await callback.message.answer_document(FSInputFile(file_path_single))
            
            files_to_remove.extend([file_path_zip, file_path_single])
        
        else:
            file_path = document_utils.generate_output(template_path, user_data_file_path, output_type)
            await callback.message.answer_document(FSInputFile(file_path))
            files_to_remove.append(file_path)

        await wait_msg.delete()
        logger.info(f"Sent output to user {user_id} ({username})")

    except Exception as e:
        logger.error(f"Error generating document for user {user_id}: {e}")
        await wait_msg.delete()
        await callback.message.answer("❌ Произошла ошибка при генерации документа. Пожалуйста, проверьте данные и шаблон.")
        
    finally:
        directory_utils.remove_temp_files(files_to_remove)
        await state.clear()