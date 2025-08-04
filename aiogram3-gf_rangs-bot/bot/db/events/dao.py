from bot.db.dao.base import BaseDAO
from bot.db.events.models import Event, Role, UserEventRole

class EventDAO(BaseDAO):
    model = Event
    
class RoleDAO(BaseDAO):
    model = Role

class UserEventRoleDAO(BaseDAO):
    model = UserEventRole
