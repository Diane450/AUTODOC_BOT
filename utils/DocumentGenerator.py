from openpyxl import load_workbook
from docxtpl import DocxTemplate
import datetime

class DocumentGenerator():
    
    def generate_document(template_path:str, data_path:str):
        template = DocxTemplate(template_path)

        workbook = load_workbook(data_path)
        sheet = workbook.active

        headers = [cell.value for cell in sheet[1]]

        for row in sheet.iter_rows(min_row=2, values_only=True):
            context = dict(zip(headers, row))

            template.render(context)

            filename_key = context.get("DOC_NAME", f"{datetime.datetime.date} - {datetime.datetime.time}")
            output_filename = f"{filename_key}.docx"

            template.save(output_filename)
            print(f"Создан файл: {output_filename}")