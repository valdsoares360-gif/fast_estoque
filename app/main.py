from fastapi import FastAPI

from rotas import usuarios, auth, produtos, movimentacoes,vs

from banco.db import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Controle de Estoque"
)

app.include_router(usuarios.router)
app.include_router(auth.router)
app.include_router(produtos.router)
app.include_router(movimentacoes.router)
app.include_router(vs.router)
@app.get("/")
def raiz():
    return {"mensagem": "API funcionando"}