from functools import wraps

from aiogram import types

from bot.db.users.dao import UserDAO
from utils.check_admin_tg_id import check_admin_tg_id

def admin_required(func):
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        user_id = message.from_user.id
        user = await UserDAO.find_one_or_none(tg_id=user_id)

        if user and check_admin_tg_id(user.tg_id):
            return await func(message, *args, **kwargs)
        else:
            await message.answer('Нет прав!')
            return
    return wrapper
