from sqlalchemy import Column, Integer, Date

from .database import Base


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, index=True)
    date = Column(Date)
    quantity = Column(Integer)