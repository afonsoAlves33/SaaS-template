from sqlalchemy import Column, Integer, String
from project.db.base import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    password = Column(String(255), unique=True)