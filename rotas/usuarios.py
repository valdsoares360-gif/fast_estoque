from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from banco.db import get_db
from modelos.usuarios import Usuario
from esquemas.usuario import UsuarioCriar, UsuarioResposta
from nucleo.seguranca import gerar_hash_senha
from nucleo.auth import get_usuario_atual

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.post("/", response_model=UsuarioResposta)
def criar_usuario(
    usuario: UsuarioCriar,
    db: Session = Depends(get_db)
):

    senha_hash = gerar_hash_senha(usuario.senha)

    novo_usuario = Usuario(
        email=usuario.email,
        senha_hash=senha_hash
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario

@router.get("/me")
def usuario_logado(usuario: Usuario = Depends(get_usuario_atual)):
    return usuario