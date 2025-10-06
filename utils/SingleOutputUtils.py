import datetime
from docxcompose.composer import Composer
from docx import Document
from utils.Logger import logger

class SingleOutputUtils:
    def create_single_output_type(self, temp_files:list):
        master_doc = Document(temp_files[0])
        composer = Composer(master_doc)
        
        combined_filename = self.create_combined_filename()
        composer = self.append_files(temp_files, composer)
        
        composer.save(combined_filename)
        logger.info(f"File {combined_filename} has been created")
        return combined_filename
    

    def append_files(self, temp_files, composer):
        for f in temp_files[1:]:
            composer.append(Document(f))
        return composer


    def create_combined_filename(self):
        return f"temp/combined_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.docx"