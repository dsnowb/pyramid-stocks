from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from .meta import Base
from sqlalchemy.exc import DBAPIError
from cryptacular import bcrypt

manager = bcrypt.BCRYPTPasswordManager()

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    password = Column(Text)
    email = Column(Text)
    username = Column(Text, unique=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = manager.encode(password, 10)

    @classmethod
    def check_credentials(cls, request=None, username=None, password=None):
        if request.dbsession is None:
            raise DBAPIError

        query = request.dbsession.query(cls).filter(cls.username == username).one_or_none()

        if query is not None:
            if manager.check(query.password, password):
                return (True, username)

        return (False, username)
