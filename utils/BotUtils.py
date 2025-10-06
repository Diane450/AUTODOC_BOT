from aiogram.types import Document as Doc
from aiogram import Bot
import datetime
from utils.Logger import logger

class BotUtils:
    
    def get_text_for_output_type(self, output_type):
            
            if output_type == "zip":
                return "Ваши документы будут присланы в ZIP архиве"
            return "Ваши документы будут присланы в едином файле"
    

    async def download_file(self, bot: Bot, doc: Doc):
        try:
            file = await bot.get_file(doc.file_id)
            temp_file_path = self.create_temp_path_users_documents(doc)
            await bot.download_file(file.file_path, temp_file_path)
            logger.info(f"Download file {file.file_path} to {temp_file_path} successfully")
            return temp_file_path
        except Exception as e:
            logger.exception(f"Exception in download_file: {e}")
    

    def create_temp_path_users_documents(self, doc: Doc):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = f"temp/{timestamp} - {doc.file_name}"
        return file_path