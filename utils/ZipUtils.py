import datetime
import zipfile
import os
class ZipUtils:
        
    def create_zip(self, temp_files:list):
        zip_filename = self.create_zip_filename()
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in temp_files:
                zipf.write(file, os.path.basename(file))
        return zip_filename
    

    def create_zip_filename(self):
        return f"temp/documents_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"