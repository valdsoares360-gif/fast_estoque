from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from banco.db import get_db
from modelos.movimentacao import Movimentacao
from modelos.produtos import Produto
from esquemas.movimentacao import MovimentacaoCreate
from nucleo.auth import get_usuario_atual
from nucleo.alerta_estoque import enviar_alerta

router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])


@router.post("/")
def registrar_movimentacao(
    mov: MovimentacaoCreate,
    db: Session = Depends(get_db),
    usuario = Depends(get_usuario_atual)
):

    produto = db.query(Produto).filter(
        Produto.id == mov.produto_id,
        Produto.usuario_id == usuario.id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    if mov.tipo == "entrada":

        produto.quantidade += mov.quantidade

    elif mov.tipo == "saida":

        if produto.quantidade < mov.quantidade:

            raise HTTPException(
                status_code=400,
                detail="Estoque insuficiente"
            )

        produto.quantidade -= mov.quantidade

    else:

        raise HTTPException(
            status_code=400,
            detail="Tipo inválido"
        )

    movimentacao = Movimentacao(
       
        produto_id=produto.id,
        tipo=mov.tipo,
        quantidade=mov.quantidade,
        data=datetime.utcnow()
    )

    db.add(movimentacao)
    db.commit()

    
    if produto.quantidade <= produto.estoque_minimo:

        enviar_alerta(produto, usuario)

    return {"mensagem": "Movimentação registrada com sucesso"}


@router.get("/")
def listar_movimentacoes(
    db: Session = Depends(get_db),
    usuario = Depends(get_usuario_atual)
):

    movs = db.query(Movimentacao, Produto).join(Produto).filter(
        Produto.usuario_id == usuario.id
    ).order_by(Movimentacao.data.desc()).limit(10).all()

    resultado = []

    for mov, produto in movs:

        resultado.append({
            "id": mov.id,
            "produto_id": produto.id,
            "produto_nome": produto.nome,
            "tipo": mov.tipo,
            "quantidade": mov.quantidade,
            "data": mov.data
        })

    return resultado