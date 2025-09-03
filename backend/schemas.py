from pydantic import BaseModel, Field
import datetime
from typing import Optional, Literal
from enum import Enum

class AssetType(str, Enum):
    STOCK="STOCK"; ETF="ETF"; FII="FII"; CRYPTO="CRYPTO"

# ----- Assets -----
class AssetBase(BaseModel):
    ticker: str = Field(min_length=1)
    name: Optional[str] = None
    type: AssetType

class AssetCreate(AssetBase): pass

class AssetUpdate(BaseModel):
    ticker: Optional[str] = None
    name: Optional[str] = None
    type: Optional[AssetType] = None

class AssetOut(AssetBase):
    id: int
    class Config: from_attributes = True

# ----- Transactions -----
class TransactionBase(BaseModel):
    asset_id: int
    operation: Literal["BUY","SELL"]
    quantity: float
    price: float
    date: datetime.date

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    operation: Optional[Literal["BUY", "SELL"]] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    date: Optional[datetime.date] = None

class TransactionOut(TransactionBase):
    id: int
    asset: AssetOut
    class Config: from_attributes = True

class PortfolioSummary(BaseModel):
    ticker: str
    name: str | None
    net_quantity: float
    avg_price: float
