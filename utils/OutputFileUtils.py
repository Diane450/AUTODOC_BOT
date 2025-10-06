from docxtpl import DocxTemplate
from utils.Logger import logger 

import datetime

class OutputFileUtils:

    def create_filename(self, context:dict):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
            filename_key = context.get("DOC_NAME", f"{timestamp}")
            output_filename = f"temp/{filename_key}.docx"
            logger.info(f"File_name {output_filename} has been created")
            return output_filename
        except Exception as e:
            logger.exception(f"EXCEPTION in create_filename: {e}")
    
    
    def generate_one_document(self, context, template_path):
        template = DocxTemplate(template_path)
        template.render(context)
        logger.info(f"File has been created")
        return template