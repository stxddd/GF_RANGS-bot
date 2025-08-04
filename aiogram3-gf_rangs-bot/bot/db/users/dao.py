from bot.db.dao.base import BaseDAO
from bot.db.users.models import User
from sqlalchemy import func, select

from bot.db.database import async_session_maker
from bot.db.events.models import UserEventRole, Role
            
class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def get_total_points_by_user_id(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(func.coalesce(func.sum(Role.points), 0))
                .select_from(UserEventRole)  # Указываем, с какой таблицы начинаем
                .join(Role, Role.id == UserEventRole.role_id)
                .filter(UserEventRole.user_id == user_id)
            )
            result = await session.execute(query)
            return result.scalar() 