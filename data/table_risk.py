from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Float, Boolean, ForeignKey


Base = declarative_base()

class cppi(Base):
    __tablename__ = 'cppi'
    date = Column(String)
    price = Column(Float)
    quantity = Column(Float)
    
    m = Column(Float)
    floor_value = Column(Float)
    cushion = Column(Float)
    drawdown = Column(Float)
    
    risky_w = Column(Float)
    safe_w = Column(Float)
    
    risky_value = Column(Float)
    safe_value = Column(Float)
    
    status = Column(String)
    value = Column(Float)
    
    
    def __init__(self, add):
        self.date = add["date"]
        self.price = add["price"]
        self.quantity = add["quantity"]
        
        self.m = add["m"]
        self.floor_value = add["floor_value"]
        self.cushion = add["cushion"]
        
        self.drawdown = add["drawdown"]
        
        self.risky_w = add["risky_w"]
        self.safe_w = add["safe_w"]
        
        self.risky_value = add["risky_value"]
        self.safe_value = add["safe_value"]
        
        self.status = add["status"]
        self.value = add["value"]
        
        
        
    
    
    