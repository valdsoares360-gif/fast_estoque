from fastapi import FastAPI

from rotas import usuarios, auth, produtos, movimentacoes

from banco.db import engine, Base
from modelos.movimentacao import Movimentacao
from modelos.usuarios import Usuario
from modelos.produtos import Produto

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Controle de Estoque"
)

app.include_router(usuarios.router)
app.include_router(auth.router)
app.include_router(produtos.router)
app.include_router(movimentacoes.router)

@app.get("/")
def raiz():
    return {"mensagem": "API funcionando"}