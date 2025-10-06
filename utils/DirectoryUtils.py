import os
import shutil
from utils.Logger import logger 
import config

class DirectoryUtils:

    def create_folder(self):
        try:
            os.makedirs(config.FOLDER_NAME, exist_ok=True)
            logger.info(f"Folder has been created: {config.FOLDER_NAME}")
        except Exception as e:
            logger.exception(f"Error in create_folder: {e}")

    def remove_temp_files(self, files:list[str]):
        try:
            if os.path.exists(config.FOLDER_NAME):
                for file_path in files:
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            logger.info(f"🧹 Deleted temp file: {file_path}")
                        else:
                            logger.warning(f"⚠️ File not found (skipped): {file_path}")
                    except Exception as e:
                        logger.exception(f"❌ Error deleting file {file_path}: {e}")
        except Exception as e:
            logger.exception(f"Error in remove_temp_files: {e}")