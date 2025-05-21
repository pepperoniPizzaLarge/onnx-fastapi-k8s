from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .db import Base


class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String, unique=True)
    last_name = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)


class Organization(Base):
    __tablename__ = 'organizations'
    
    id = Column(Integer, primary_key=True, index=True)
    org_name = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))