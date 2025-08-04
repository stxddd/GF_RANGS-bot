from sqlalchemy import BigInteger, Column, String, Integer, Boolean
from bot.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False, unique=True)
    
    fullname = Column(String(150), nullable = False)
    course_number = Column(Integer, nullable = False)
    group_number = Column(String(32), nullable = False)