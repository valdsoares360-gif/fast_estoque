from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from banco.db import get_db
from modelos.movimentacao import Movimentacao
from modelos.produtos import Produto
from esquemas.movimentacao import MovimentacaoCreate
from nucleo.auth import get_usuario_atual
from nucleo.alerta_estoque import enviar_alerta

router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])


@router.post("/")
def criar_movimentacao(
    movimentacao: MovimentacaoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual)
):

    produto = db.query(Produto).filter(
        Produto.id == movimentacao.produto_id
    ).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if movimentacao.tipo == "entrada":
        produto.quantidade += movimentacao.quantidade

    elif movimentacao.tipo == "saida":

        if produto.quantidade < movimentacao.quantidade:
            raise HTTPException(status_code=400, detail="Estoque insuficiente")

        produto.quantidade -= movimentacao.quantidade

    else:
        raise HTTPException(status_code=400, detail="Tipo inválido")

    nova_movimentacao = Movimentacao(**movimentacao.dict())

    db.add(nova_movimentacao)

    db.commit()
    if produto.quantidade <= produto.estoque_minimo:
       enviar_alerta(produto)

    return nova_movimentacao


@router.get("/")
def listar_movimentacoes(
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual)
):
    return db.query(Movimentacao).all()