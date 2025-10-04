from openpyxl import load_workbook
from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from docx import Document
import datetime
import zipfile
import os

class DocumentGenerator:
    def generate_document(self, template_path: str, data_path: str, output_type: str):
        # Создаём временную папку, если её нет
        os.makedirs("temp", exist_ok=True)

        # Открываем Excel с вычисленными значениями формул
        workbook = load_workbook(data_path, data_only=True)
        sheet = workbook.active

        # Считываем заголовки
        headers = [cell.value for cell in sheet[1]]
        temp_files = []

        # Проходим по строкам данных
        for row in sheet.iter_rows(min_row=2):
            clean_row = []

            for cell in row:
                value = cell.value

                # Обработка дат и времени
                if isinstance(value, datetime.datetime):
                    fmt = str(cell.number_format).lower()

                    # Если в формате есть "h" или "ч" → значит, пользователь ввёл время
                    if "h" in fmt or "ч" in fmt:
                        value = value.strftime("%d.%m.%Y %H:%M")
                    else:
                        value = value.strftime("%d.%m.%Y")

                elif isinstance(value, datetime.date):
                    value = value.strftime("%d.%m.%Y")

                clean_row.append(value)

            # Сопоставляем заголовки и значения
            context = dict(zip(headers, clean_row))

            # Генерируем DOCX по шаблону
            template = DocxTemplate(template_path)
            template.render(context)

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename_key = context.get("DOC_NAME", f"{timestamp}")
            output_filename = f"temp/{filename_key}.docx"

            template.save(output_filename)
            temp_files.append(output_filename)
            print(f"✅ Создан файл: {output_filename}")

        # --- Сборка ZIP ---
        if output_type == "zip":
            zip_filename = f"temp/documents_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in temp_files:
                    zipf.write(file, os.path.basename(file))
            print(f"📦 Создан архив: {zip_filename}")
            return zip_filename

        # --- Сборка единого документа ---
        elif output_type == "single":
            if not temp_files:
                print("⚠️ Нет файлов для объединения.")
                return None

            master_doc = Document(temp_files[0])
            composer = Composer(master_doc)

            for f in temp_files[1:]:
                doc_to_append = Document(f)
                composer.append(doc_to_append)

            combined_filename = f"temp/combined_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.docx"
            composer.save(combined_filename)

            print(f"🧩 Создан единый файл: {combined_filename}")
            return combined_filename

        else:
            print("❌ Неизвестный тип вывода. Используйте 'zip' или 'single'.")
            return None
