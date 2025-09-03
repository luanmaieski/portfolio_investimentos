# backend/app/routers/transactions.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import TransactionCreate, TransactionUpdate, TransactionOut, TransactionBase, PortfolioSummary
from crud import transactions as crud

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionOut)
def create_tx(data: TransactionCreate, db: Session = Depends(get_db)):
    return crud.create(db, data)

@router.get("/", response_model=list[TransactionOut])
def list_txs(asset_id: int | None = Query(default=None), db: Session = Depends(get_db)):
    """Retorna a lista de transações"""
    return crud.list_(db, asset_id)

@router.get("/summary", response_model=list[PortfolioSummary])
def portfolio_summary(db: Session = Depends(get_db)):
    return crud.get_summary(db)

@router.get("/{id}", response_model=TransactionOut)
def get_tx(id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, id)
    if not obj:
        raise HTTPException(404, "Transaction not found")
    return obj

@router.patch("/{id}", response_model=TransactionOut)
def update_tx(id: int, data: TransactionUpdate, db: Session = Depends(get_db)):
    obj = crud.update(db, id, data)
    if not obj:
        raise HTTPException(404, "Transaction not found")
    return obj

@router.delete("/{id}", status_code=204)
def delete_tx(id: int, db: Session = Depends(get_db)):
    ok = crud.delete(db, id)
    if not ok:
        raise HTTPException(404, "Transaction not found")


@router.get("/realized/", response_model=list[dict])
def realized_summary(db: Session = Depends(get_db)):
    return crud.get_realized_profit(db)
