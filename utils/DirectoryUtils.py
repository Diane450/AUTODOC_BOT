import os
import shutil


class DirectoryUtils:

    def create_folder(self, folder_name="temp"):
        os.makedirs(folder_name, exist_ok=True)

    def remove_temp_files(self, folder_path="temp"):
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print("✅Временные файлы удалены✅")