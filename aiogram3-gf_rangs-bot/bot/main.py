import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from bot.handlers.register import router as register_router
from bot.handlers.admin_handlers.event_manager import router as add_event_router
from bot.handlers.admin_handlers.role_manager import router as add_role_router
from bot.handlers.delete_last_message import router as delete_last_message_router
from bot.handlers.admin_handlers.user_manager import router as user_manager_router
from bot.handlers.my_points import router as my_points_router
from bot.handlers.get_points import router as get_points_router
from bot.handlers.condition import router as condition_router
from bot.handlers.edit_profile import router as edit_profile_router
from utils.db_backup_notification import send_backup

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=settings.BOT_API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    asyncio.create_task(send_backup(bot))
    dp.include_routers(
        register_router,
        add_event_router,
        add_role_router,
        delete_last_message_router,
        user_manager_router,
        my_points_router,
        get_points_router,
        condition_router,
        edit_profile_router
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
