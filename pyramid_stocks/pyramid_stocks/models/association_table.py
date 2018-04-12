from sqlalchemy.orm import relationship
from sqlalchemy import (
    Table,
    Column,
    Integer,
    ForeignKey,
)

from .meta import Base

association_table = Table('association_table', Base.metadata,
    Column('account_id', Integer, ForeignKey('accounts.id')),
    Column('stock_id', Integer, ForeignKey('stocks.id')),
)
