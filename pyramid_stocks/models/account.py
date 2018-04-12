from .association_table import association_table
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text
from .meta import Base
from sqlalchemy.exc import DBAPIError
from cryptacular import bcrypt

manager = bcrypt.BCRYPTPasswordManager()

class Account(Base):
    '''ORM model for user accounts'''

    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    password = Column(Text)
    email = Column(Text)
    username = Column(Text, unique=True)
    stock_id = relationship('Stock', secondary=association_table, back_populates='account_id')

    def __init__(self, username, email, password):
        '''Init a user account object, and encode the password, salting 10 times'''

        self.username = username
        self.email = email
        self.password = manager.encode(password, 10)

    @classmethod
    def check_credentials(cls, request=None, username=None, password=None):
        '''Verify passed user credentials'''

        if request.dbsession is None:
            raise DBAPIError

        query = request.dbsession.query(cls).filter(cls.username == username).one_or_none()

        if query is not None:
            if manager.check(query.password, password):
                return (True, username)

        return (False, username)
