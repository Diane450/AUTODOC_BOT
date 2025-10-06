import os
import time
import asyncio
from utils.Logger import logger

TEMP_DIR = "temp"

async def clean_old_temp_files(interval_hours: int = 6, max_age_seconds: int = 3600):
    while True:
        now = time.time()
        deleted_files = 0

        if os.path.exists(TEMP_DIR):
            for filename in os.listdir(TEMP_DIR):
                file_path = os.path.join(TEMP_DIR, filename)
                if os.path.isfile(file_path):
                    file_age = now - os.path.getmtime(file_path)
                    if file_age > max_age_seconds:
                        os.remove(file_path)
                        deleted_files += 1

        if deleted_files:
            logger.info(f"🧹 Cleaned {deleted_files} old temp files")

        await asyncio.sleep(interval_hours * 3600)
