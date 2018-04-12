from .association_table import association_table
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text
from .meta import Base


class Stock(Base):
    '''ORM model of a stock'''

    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    symbol = Column(Text, unique=True)
    companyName = Column(Text, default=None)
    exchange = Column(Text, default=None)
    industry = Column(Text, default=None)
    website = Column(Text, default=None)
    description = Column(Text, default=None)
    CEO = Column(Text, default=None)
    issueType = Column(Text, default=None)
    sector = Column(Text, default=None)

    account_id = relationship('Account',secondary=association_table, back_populates='stock_id')
