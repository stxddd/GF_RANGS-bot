from sqlalchemy import BigInteger, Column, String, Integer, Boolean, Date
from bot.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False, unique=True)
    
    fullname = Column(String(150), nullable = False)
    course_number = Column(Integer, nullable = False)
    group_number = Column(String(32), nullable = False)
    is_approved = Column(Boolean, nullable = True)
    attempt_count = Column(Integer, nullable=True, default=0)
    last_attempt_date = Column(Date, nullable=True)