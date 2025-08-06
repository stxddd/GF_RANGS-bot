import asyncio
import logging
from datetime import datetime, timedelta
import os

from aiogram.types import FSInputFile

from config import settings


logger = logging.getLogger(__name__)

async def send_backup(bot):
    while True:
        now = datetime.now()
        next_run = now.replace(
            hour=settings.HOUR_TO_RECEIVE_NOTIFICATIONS,
            minute=settings.MINUTE_TO_RECEIVE_NOTIFICATIONS,
            second=0,
            microsecond=0,
        )

        if now >= next_run:
            next_run += timedelta(days=1)

        sleep_time = (next_run - now).total_seconds()
        
        logger.info(f"Через {sleep_time} секунд прийдет бекап БД")

        await asyncio.sleep(sleep_time)

        file_path = "bot/db/backup.sql"

        if not os.path.exists(file_path):
            for admin_tg_id in str(settings.ADMIN_TG_IDS).split(','):
                await bot.send_message(int(admin_tg_id), "Ошибка бекапа.")
            return

        backup_file = FSInputFile(file_path)
        
        for admin_tg_id in str(settings.ADMIN_TG_IDS).split(','):
                await bot.send_document(admin_tg_id, backup_file)
        return
        