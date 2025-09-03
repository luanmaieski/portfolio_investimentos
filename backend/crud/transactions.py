# backend/app/crud/transactions.py
from sqlalchemy.orm import Session
from sqlalchemy import select, func, case
from models import Transaction, Asset
from schemas import TransactionCreate, TransactionUpdate, TransactionOut

def create(db: Session, data: TransactionCreate) -> Transaction:
    obj = Transaction(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get(db: Session, tx_id: int) -> Transaction | None:
    return db.get(Transaction, tx_id)

def list_(db: Session, asset_id: int | None = None) -> list[Transaction]:
    stmt = select(Transaction)
    if asset_id is not None:
        stmt = stmt.where(Transaction.asset_id == asset_id)
    return db.scalars(stmt).all()

def update(db: Session, tx_id: int, data: TransactionUpdate) -> Transaction | None:
    obj = db.get(Transaction, tx_id)
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, tx_id: int) -> bool:
    obj = db.get(Transaction, tx_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

def get_summary(db: Session):
    buy_qty = func.coalesce(
        func.sum(case((Transaction.operation == "BUY", Transaction.quantity), else_=0.0)),
        0.0
    ).label("buy_qty")

    sell_qty = func.coalesce(
        func.sum(case((Transaction.operation == "SELL", Transaction.quantity), else_=0.0)),
        0.0
    ).label("sell_qty")

    net_quantity = (buy_qty - sell_qty).label("net_quantity")

    buy_value = func.coalesce(
        func.sum(case(
            (Transaction.operation == "BUY", Transaction.quantity * Transaction.price),
            else_=0.0
        )),
        0.0
    )

    avg_buy_price = (buy_value / func.nullif(buy_qty, 0.0)).label("avg_buy_price")

    rows = (
        db.query(
            Asset.id.label("asset_id"),
            Asset.ticker.label("ticker"),
            Asset.name.label("name"),
            net_quantity,
            avg_buy_price,
        )
        .join(Transaction, Transaction.asset_id == Asset.id)
        .group_by(Asset.id, Asset.ticker, Asset.name)
        .all()
    )

    summary = []
    for row in rows:
        m = row._mapping  # <- forma segura/estável no SA 2.x
        summary.append({
            "asset_id": m["asset_id"],
            "ticker": m["ticker"],
            "name": m["name"],
            "net_quantity": float(m["net_quantity"] or 0),
            "avg_price": float(m["avg_buy_price"] or 0),
        })
    return summary


def get_realized_profit(db: Session):
    txs = db.query(Transaction).join(Asset).order_by(Transaction.date).all()

    positions = {}  # {asset_id: {"qty": float, "avg_price": float, "profit": float, "ticker": str}}
    realized = []

    for tx in txs:
        asset_id = tx.asset_id
        if asset_id not in positions:
            positions[asset_id] = {"qty": 0, "avg_price": 0, "profit": 0, "ticker": tx.asset.ticker}

        pos = positions[asset_id]

        if tx.operation == "BUY":
            # recalcula preço médio ponderado
            total_cost = pos["qty"] * pos["avg_price"] + tx.quantity * tx.price
            pos["qty"] += tx.quantity
            pos["avg_price"] = total_cost / pos["qty"]

        elif tx.operation == "SELL":
            if pos["qty"] <= 0:
                # opcional: ignorar vendas sem posição (evita short selling)
                continue

            sell_qty = min(tx.quantity, pos["qty"])  # não vender mais do que tem
            lucro = (tx.price - pos["avg_price"]) * sell_qty

            pos["qty"] -= sell_qty
            pos["profit"] += lucro

            # se ainda houver quantidade na venda que não foi casada, ignora

    # resumo final
    for asset_id, pos in positions.items():
        realized.append({
            "ticker": pos["ticker"],
            "realized_profit": pos["profit"]
        })

    return realized
