from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from banco.db import get_db
from modelos.produtos import Produto
from modelos.movimentacao import Movimentacao

from esquemas.produto import ProdutoCreate
from nucleo.auth import get_usuario_atual




router = APIRouter(prefix="/produtos", tags=["Produtos"])




@router.post("/")
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario = Depends(get_usuario_atual)
):

    novo_produto = Produto(
        nome=produto.nome,
        descricao=produto.descricao,
        quantidade=produto.quantidade,
        preco=produto.preco,
        estoque_minimo=produto.estoque_minimo,
        usuario_id=usuario.id
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto




@router.get("/")
def listar_produtos(
    db: Session = Depends(get_db),
    usuario = Depends(get_usuario_atual)
):

    produtos = db.query(Produto).filter(
        Produto.usuario_id == usuario.id
    ).all()

    return produtos




@router.get("/{produto_id}")
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(get_usuario_atual)
):

    produto = db.query(Produto).filter(
        Produto.id == produto_id,
        Produto.usuario_id == usuario.id
    ).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return produto




@router.delete("/{produto_id}")
def deletar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(get_usuario_atual)
):

    produto = db.query(Produto).filter(
        Produto.id == produto_id,
        Produto.usuario_id == usuario.id
    ).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    movimentacoes = db.query(Movimentacao).filter(
        Movimentacao.produto_id == produto_id
    ).first()

    if movimentacoes:
        raise HTTPException(
            status_code=400,
            detail="Não é possível deletar produto que possui movimentações"
        )

    db.delete(produto)
    db.commit()

    return {"mensagem": "Produto deletado com sucesso"}




@router.put("/{produto_id}")
def atualizar_produto(
    produto_id: int,
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario = Depends(get_usuario_atual)
):

    produto_db = db.query(Produto).filter(
        Produto.id == produto_id,
        Produto.usuario_id == usuario.id
    ).first()

    if not produto_db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    produto_db.nome = produto.nome
    produto_db.descricao = produto.descricao
    produto_db.quantidade = produto.quantidade
    produto_db.preco = produto.preco
    produto_db.estoque_minimo = produto.estoque_minimo

    db.commit()
    db.refresh(produto_db)

    return produto_db