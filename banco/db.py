from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://estoque_user:senha123@localhost:5432/controle_estoque"

engine = create_engine(DATABASE_URL)

SessaoLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessaoLocal()
    try:
        yield db
    finally:
        db.close()