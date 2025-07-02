from sqlalchemy import Column, Integer, String
from app.database.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user") 

class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer,primary_key=True, index=True)