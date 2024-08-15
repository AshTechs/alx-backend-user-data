#!/usr/bin/env python3
"""auth"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from typing import TypeVar
from uuid import uuid4


def _hash_password(password: str) -> str:
    """_hash_password

    Args:
        password (str):

    Returns:
        str: hashed Password
    """
    salt = bcrypt.gensalt()
    code_password = password.encode('utf-8')
    hashedPassword = bcrypt.hashpw(code_password, salt)
    return hashedPassword


def _generate_uuid() -> str:
    """_generate_uuid

    Returns:
        str: new  uuid
    """
    new_uuid = str(uuid4())
    return new_uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> str:
        """register_user

        Args:
            email (str):
            password (str):

        Raises:
            ValueError: User <user's email> already exists

        Returns:
            str: user
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hash_password = _hash_password(password)
            user = self._db.add_user(
                email=email, hashed_password=hash_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """valid_login

        Args:
            email (str):
            password (str):

        Returns:
            bool:
        """
        try:
            user = self._db.find_user_by(email=email)
            p = password.encode("utf-8")
            check_pass = bcrypt.checkpw(p, user.hashed_password)
            return check_pass
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """create_session

        Args:
            email (str):

        Returns:
            str: new id
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        self._db.update_user(user.id, session_id=_generate_uuid())
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> str:
        """get_user_from_session_id

        Args:
            session_id (str):

        Returns:
            str: user
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy_session

        Args:
            user_id (int):

        Returns:
            None:
        """
        if user_id is None:
            return None
        else:
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """get_reset_password_token

        Args:
            email (str):

        Raises:
            ValueError:

        Returns:
            str: token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        self._db.update_user(user.id, reset_token=_generate_uuid())
        return user.reset_token

    def update_password(self, reset_token: str, password: str) -> str:
        """update_password

        Args:
            reset_token (str):
            password (str):

        Raises:
            ValueError:

        Returns:
            None:
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            pwd = _hash_password(password)
            self._db.update_user(
                user.id,
                hashed_password=pwd,
                reset_token=None)
            return None
        except Exception:
            raise ValueError
