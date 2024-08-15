#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import User
from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add_user

        Args:
            email (str):
            hashed_password (str):

        Returns:
            User:
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """find_user_by

        Raises:
            NoResultFound:

        Returns:
            User:
        """
        user_query = self._session.query(User).filter_by(**kwargs)
        user = user_query.first()
        if user is None:
            raise NoResultFound
        else:
            return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """update_user

        Args:
            user_id (int):

        Raises:
            ValueError:

        Returns:
            None:
        """
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            dict_users = user.__dict__
            if k in dict_users:
                setattr(user, k, v)
            else:
                raise ValueError
        self._session.commit()
        return None
