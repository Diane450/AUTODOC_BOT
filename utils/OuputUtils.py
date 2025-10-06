from utils.SpreadSheetUtils import SpreadSheetUtils
from utils.ExcelUtils import ExcelUtils
from utils.ZipUtils import ZipUtils
from utils.SingleOutputUtils import SingleOutputUtils
from utils.OutputFileUtils import OutputFileUtils
from utils.DirectoryUtils import DirectoryUtils
from utils.Logger import logger

spreadsheet_utils = SpreadSheetUtils()
excel_utils = ExcelUtils()
zip_utils = ZipUtils()
singleoutput_utils = SingleOutputUtils()
output_file_utils = OutputFileUtils()
directory_file_utils = DirectoryUtils()

class OutputUtils:

    def _load_data(self, data_path: str):
        
        if "docs.google.com/spreadsheets" in data_path:
            headers, rows = spreadsheet_utils.load_data(data_path)
        else:
            headers, rows = excel_utils.load_data(data_path)
        logger.info(f"Get headers & rows successfully")
        return headers, rows


    def generate_output(self, template_path: str, data_path: str, output_type: str):
        headers, rows = self._load_data(data_path)

        temp_files = self.generate_documents(rows, headers, template_path)

        if output_type == "zip":
            zip_filename = zip_utils.create_zip(temp_files)
            directory_file_utils.remove_temp_files(temp_files)
            return zip_filename

        elif output_type == "single":
            combined_filename = singleoutput_utils.create_single_output_type(temp_files)
            directory_file_utils.remove_temp_files(temp_files)
            return combined_filename


    def generate_documents(self, rows, headers, template_path):
        temp_files = []
        for row in rows:
            context = dict(zip(headers, row))

            template = output_file_utils.generate_one_document(context, template_path)

            output_filename = output_file_utils.create_filename(context)

            template.save(output_filename)
            temp_files.append(output_filename)

            logger.info(f"File {output_filename} saved")

        return temp_files