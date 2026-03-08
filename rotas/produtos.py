from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from banco.db import get_db
from modelos.produtos import Produto
from esquemas.produto import ProdutoCreate
from nucleo.auth import get_usuario_atual

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("/")
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual)
):
    novo_produto = Produto(**produto.dict())

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


@router.get("/")
def listar_produtos(
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual)
):
    return db.query(Produto).all()


@router.get("/{produto_id}")
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual)
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return produto


@router.delete("/{produto_id}")
def deletar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual)
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(produto)
    db.commit()

    return {"mensagem": "Produto deletado"}