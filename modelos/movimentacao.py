from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from banco.db import Base


class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True, index=True)

    produto_id = Column(Integer, ForeignKey("produtos.id"))

    tipo = Column(String, nullable=False)  # entrada ou saida

    quantidade = Column(Integer, nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    data = Column(DateTime(timezone=True), server_default=func.now())