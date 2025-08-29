from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, Literal
from enum import Enum

class AssetType(str, Enum):
    STOCK="STOCK"; ETF="ETF"; FII="FII"; CRYPTO="CRYPTO"

class AssetBase(BaseModel):
    ticker: str = Field(min_length=1)
    name: Optional[str] = None
    type: AssetType

class AssetCreate(AssetBase): pass
class AssetOut(AssetBase):
    id: int
    class Config: from_attributes = True

class TransactionBase(BaseModel):
    asset_id: int
    operation: Literal["BUY","SELL"]
    quantity: float
    price: float
    fees: Optional[float] = 0.0
    date: date

class TransactionCreate(TransactionBase): pass
class TransactionOut(TransactionBase):
    id: int
    class Config: from_attributes = True

class PriceOut(BaseModel):
    id: int
    asset_id: int
    date: date
    close: float
    source: str
    class Config: from_attributes = True
