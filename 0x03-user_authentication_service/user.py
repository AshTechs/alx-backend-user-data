#!/usr/bin/env python3
"""
User model for the users table.
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class User(Base):
    """
    SQLAlchemy model for the users table.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)


# Optional: If you want to create an SQLite database for testing
if __name__ == "__main__":
    engine = create_engine('sqlite:///test.db')
    Base.metadata.create_all(engine)

    # Optional: Example of how to create a session
    Session = sessionmaker(bind=engine)
    session = Session()
