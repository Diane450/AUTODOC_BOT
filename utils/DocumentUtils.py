from openpyxl import load_workbook
from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from docx import Document
from aiogram.types import Document as Doc
from aiogram import Bot
from utils.SpreadSheetUtils import SpreadSheetUtils
from utils.ExcelUtils import ExcelUtils
import pandas as pd
import datetime
import zipfile
import os

spreadsheet_utils = SpreadSheetUtils()
excel_utils = ExcelUtils()

class DocumentUtils:

    def _load_data(self, data_path: str):
        
        if "docs.google.com/spreadsheets" in data_path:
            headers, rows = spreadsheet_utils.load_data(data_path)
        else:
            headers, rows = excel_utils.load_data(data_path)
        return headers, rows

    def generate_document(self, template_path: str, data_path: str, output_type: str):
        headers, rows = self._load_data(data_path)
        temp_files = []

        for row in rows:
            context = dict(zip(headers, row))
            template = DocxTemplate(template_path)
            template.render(context)

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename_key = context.get("DOC_NAME", f"{timestamp}")
            output_filename = f"temp/{filename_key}.docx"

            template.save(output_filename)
            temp_files.append(output_filename)
            print(f"✅ Создан файл: {output_filename}")

        if output_type == "zip":
            zip_filename = f"temp/documents_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in temp_files:
                    zipf.write(file, os.path.basename(file))
            return zip_filename

        elif output_type == "single":
            master_doc = Document(temp_files[0])
            composer = Composer(master_doc)
            for f in temp_files[1:]:
                composer.append(Document(f))
            combined_filename = f"temp/combined_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.docx"
            composer.save(combined_filename)
            return combined_filename


    def create_temp_path(self, doc: Doc):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = f"temp/{timestamp} - {doc.file_name}"
        return file_path

    async def download_file(self, bot: Bot, doc: Doc):
        file = await bot.get_file(doc.file_id)
        temp_file_path = self.create_temp_path(doc)
        await bot.download_file(file.file_path, temp_file_path)
        return temp_file_path
