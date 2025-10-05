import pandas as pd
import datetime

class DateTimeUtils:
    def clean_value(self, value):
        """Корректно форматирует даты, время и даты с временем."""
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return ""

        # Если есть и дата, и время
        if isinstance(value, datetime.datetime):
            if value.time() == datetime.time(0, 0, 0):
                return value.strftime("%d.%m.%Y")
            else:
                return value.strftime("%d.%m.%Y %H:%M")

        # Если только дата
        if isinstance(value, datetime.date):
            return value.strftime("%d.%m.%Y")

        # Если только время
        if isinstance(value, datetime.time):
            if value == datetime.time(0, 0, 0):
                return "00:00"
            return value.strftime("%H:%M")

        return str(value)
