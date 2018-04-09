from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from .meta import Base


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    password = Column(Text)
    email = Column(Text)
    username = Column(Text)
