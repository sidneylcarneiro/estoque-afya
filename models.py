from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False, default="user")
    
    hashed_password = Column(String, nullable=True)

    stock_items_created = relationship("StockItem", back_populates="creator")

class StockItem(Base):
    __tablename__ = "stock_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_by_username = Column(String, nullable=False)

    creator = relationship("User", back_populates="stock_items_created")

class LogEntry(Base):
    __tablename__ = "log_entries"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    action = Column(String, nullable=False)
    username = Column(String, nullable=False)

