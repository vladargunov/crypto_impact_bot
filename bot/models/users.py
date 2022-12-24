from sqlalchemy import Column, Integer, String, Float, Time
from database.base import Base


class Users(Base):
    __tablename__ = "users"

    # Table columns
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    monitor = Column(Integer)

    def __repr__(self):
        repr_str = (
            f"Users(id={self.id}, chat_id={self.chat_id})" + f"monitor={self.monitor}"
        )
        return repr_str
