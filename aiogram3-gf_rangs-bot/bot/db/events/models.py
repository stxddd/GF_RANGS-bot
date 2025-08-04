from sqlalchemy import Column, String, Integer, Boolean
from bot.db.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable = False)
    visibility = Column(Boolean, nullable = False)


class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key = True)
    event_id = Column(Integer, nullable = False)
    name = Column(String(150), nullable = False)
    points= Column(Integer, nullable = False)


class UserEventRole(Base):
    __tablename__ = "user_event_role"
    
    id = Column(Integer, primary_key = True)
    event_id = Column(Integer, nullable = False)
    user_id = Column(Integer, nullable = False)
    role_id = Column(Integer, nullable = False)
    