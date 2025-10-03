from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

zip_or_document_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🗂 ZIP архив", callback_data="output_zip"),
    InlineKeyboardButton(text="📄 Один документ", callback_data="output_single")]
])