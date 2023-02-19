from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Float, Boolean, ForeignKey

from .base import Base


class Data(Base):
    __tablename__ = 'data'
    time = Column(String, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    
    def __init__(self, add):
        self.time = add['time']
        self.open = add['open']
        self.high = add['high']
        self.low = add['low']
        self.close = add['close']




        



