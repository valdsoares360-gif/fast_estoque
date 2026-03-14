from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modelos.produtos import Produto
from banco.db import get_db
from modelos.usuarios import Usuario
from nucleo.auth import get_usuario_atual

router = APIRouter(prefix="/vsbot", tags=["Vsbot"])

@router.get("/produtos-bot")
def produtos_bot(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):

    produtos = (
        db.query(Produto)
        .filter(Produto.usuario_id == usuario.id)
        .all()
    )

    return produtos