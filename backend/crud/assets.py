# backend/app/crud/assets.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Asset
from schemas import AssetCreate, AssetUpdate

def create(db: Session, data: AssetCreate) -> Asset:
    obj = Asset(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get(db: Session, asset_id: int) -> Asset | None:
    return db.get(Asset, asset_id)

def list_(db: Session) -> list[Asset]:
    return db.scalars(select(Asset)).all()

def update(db: Session, asset_id: int, data: AssetUpdate) -> Asset | None:
    obj = db.get(Asset, asset_id)
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, asset_id: int) -> bool:
    try:
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        if not asset:
            return False
        db.delete(asset)
        db.commit()
        return True
    except Exception as e:
        print(f"Erro ao deletar ativo {asset_id}: {e}")
        raise

