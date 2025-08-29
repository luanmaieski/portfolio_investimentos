from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class AssetType(str, enum.Enum):
    STOCK="STOCK"; ETF="ETF"; FII="FII"; CRYPTO="CRYPTO"

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True, nullable=False)  # ex: PETR4.SA, AAPL, BTC
    name = Column(String, nullable=True)
    type = Column(Enum(AssetType), nullable=False)
    transactions = relationship("Transaction", back_populates="asset", cascade="all,delete")
    prices = relationship("Price", back_populates="asset", cascade="all,delete")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    operation = Column(String, nullable=False)  # "BUY" | "SELL"
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    fees = Column(Float, nullable=True)
    date = Column(Date, nullable=False)
    asset = relationship("Asset", back_populates="transactions")

class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    close = Column(Float, nullable=False)
    source = Column(String, nullable=False)  # "yfinance" | "coingecko"
    asset = relationship("Asset", back_populates="prices")
