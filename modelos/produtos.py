from sqlalchemy import Column, Integer, String, Float,ForeignKey 
from banco.db import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class Produto(Base):

    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String)

    descricao = Column(String)

    quantidade = Column(Integer)

    preco = Column(Float)

    estoque_minimo = Column(Integer)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))