#!/usr/bin/env python3
"""
Auth module
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self) -> None:
        """Initialize a new Auth instance."""
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
        Hashes a password using bcrypt and returns the hashed password as bytes

        Args:
            password (str): The password to hash.

        Returns:
            bytes: The hashed password.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the provided email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the provided email already exists.
        """
        # Check if user already exists
        existing_user = self._db._session.query(User).filter_by(email=email).first()
        if existing_user:
            raise ValueError(f"User {email} already exists")

        # User does not exist, hash password and add new user
        hashed_password = self._hash_password(password)
        new_user = self._db.add_user(email, hashed_password)
        return new_user
