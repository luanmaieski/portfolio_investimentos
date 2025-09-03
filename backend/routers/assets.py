# backend/app/routers/assets.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import AssetCreate, AssetUpdate, AssetOut
from crud import assets as crud

router = APIRouter(prefix="/assets", tags=["assets"])

@router.post("/", response_model=AssetOut)
def create_asset(data: AssetCreate, db: Session = Depends(get_db)):
    """Para inserir um novo ativo na lista"""
    return crud.create(db, data)

@router.get("/", response_model=list[AssetOut])
def list_assets(db: Session = Depends(get_db)):
    """Para retornar a lista de Ativos"""
    return crud.list_(db)

@router.get("/{asset_id}", response_model=AssetOut)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    """Para retornar um Ativo específico, informe o id do ativo"""
    obj = crud.get(db, asset_id)
    if not obj:
        raise HTTPException(404, "Ativo não encontrado")
    return obj

@router.patch("/{asset_id}", response_model=AssetOut)
def update_asset(asset_id: int, data: AssetUpdate, db: Session = Depends(get_db)):
    """Para alterar informações de um ativo cadastrado, informe o id do ativo"""
    obj = crud.update(db, asset_id, data)
    if not obj:
        raise HTTPException(404, "Ativo não encontrado")
    return obj

@router.delete("/{asset_id}", status_code=204)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    """Para deletar um ativo da lista"""
    ok = crud.delete(db, asset_id)
    if not ok:
        raise HTTPException(404, "Ativo não encontrado")
    