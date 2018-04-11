from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from .meta import Base


class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    symbol = Column(Text, unique=True)
    companyName = Column(Text)
    exchange = Column(Text)
    industry = Column(Text)
    website = Column(Text)
    description = Column(Text)
    CEO = Column(Text)
    issueType = Column(Text)
    sector = Column(Text)

    def __init__(self, symbol, companyName=None, exchange=None, industry=None, website=None, description=None, CEO=None, issueType=None, sector=None):
        self.symbol = symbol
        self.companyName = companyName
        self.exchange = exchange
        self.industry = industry
        self.website = website
        self.description = description
        self.CEO = CEO
        self.issueType = issueType
        self.sector = sector
