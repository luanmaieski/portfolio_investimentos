# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import Base, engine
from routers import assets, transactions

# Cria as tabelas automaticamente (para estudo).
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Portfolio CRUD ")

# CORS
allowed_origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",")] if settings.ALLOWED_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assets.router)
app.include_router(transactions.router)

@app.get("/")
def ping():
    return {"status": "ok"}
