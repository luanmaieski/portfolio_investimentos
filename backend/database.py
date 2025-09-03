from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

#POSTGRES_DATABASE_URL = "postgresql://user:password@postgres/mydatabase"
#DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/portfolio"
engine = create_engine(settings.DATABASE_URL)
#engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base() #ORM

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
