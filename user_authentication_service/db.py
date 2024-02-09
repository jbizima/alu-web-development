#!/usr/bin/env python3
"""
SQLAlchemy model DB
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """
    DB class
    """
    valid_args = ['id', 'email', 'hashed_password',
                  'session_id', 'reset_token']

    def __init__(self):
        """
        Initialize DB
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """
        Session
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Save a user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Return the first row in the users table after filtering
        """
        if not kwargs:
            raise InvalidRequestError
        for arg in kwargs:
            if arg not in self.valid_args:
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update user attributes
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key not in self.valid_args:
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
