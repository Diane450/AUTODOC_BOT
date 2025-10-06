import pandas as pd
from pandas import DataFrame
from utils.Logger import logger

from utils.DateTimeUtils import DateTimeUtils

datetime_utils = DateTimeUtils()

class SpreadSheetUtils:
    def load_data(self, data_path):
        
        csv_url = self.get_csv_url(data_path)
        df = pd.read_csv(csv_url)

        headers = self.get_headers(df)
        rows = self.get_rows(df)

        rows = self.validate_date_and_time(rows)
        return headers, rows
    

    def validate_date_and_time(self, rows):
        clean_rows = []
        for row in rows:
            clean_row = [datetime_utils.clean_value(value) for value in row]
            clean_rows.append(clean_row)
        return clean_rows


    def get_headers(self, df:DataFrame):
        return list(df.columns)


    def get_rows(self, df:DataFrame):
        return df.values.tolist()


    def get_csv_url(self, data_path):
        sheet_id = data_path.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        logger.info(f"Got csv url from link")
        return csv_url
