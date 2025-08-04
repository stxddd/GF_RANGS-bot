from bot.db.dao.base import BaseDAO
from bot.db.users.models import User
from sqlalchemy import func, select

from bot.db.database import async_session_maker
from bot.db.events.models import UserEventRole, Role
            
class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def get_user_events_and_total_points(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(
                    UserEventRole.event_id,
                    func.sum(Role.points).label("total_points")
                )
                .join(Role, (UserEventRole.role_id == Role.id) & (UserEventRole.event_id == Role.event_id))
                .where(UserEventRole.user_id == user_id)
                .group_by(UserEventRole.event_id)
            )
            result = await session.execute(query)
            rows = result.all()  
            total_points = sum(row.total_points for row in rows)
            event_ids = [row.event_id for row in rows]
            
            return {
                "total_points": total_points,
                "event_ids": event_ids
            }