#!/usr/bin/env python3
"""
User module
"""
from sqlalchemy import Column, Integer, String, Base

Base = declarative_base()

class User(Base):
    """User class
    Represents a user in the database.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
