from docxtpl import DocxTemplate

import datetime

class OutputFileUtils:

    def create_filename(self, context:dict):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename_key = context.get("DOC_NAME", f"{timestamp}")
        output_filename = f"temp/{filename_key}.docx"
        return output_filename
    
    
    def generate_one_document(self, row, headers, context, template_path):
        template = DocxTemplate(template_path)
        template.render(context)
        return template