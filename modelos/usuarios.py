from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from banco.db import Base


class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True, nullable=False)

    senha_hash = Column(String, nullable=False)

    ativo = Column(Boolean, default=True)

    criado_em = Column(DateTime, default=datetime.utcnow)