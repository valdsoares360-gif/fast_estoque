from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from banco.db import get_db
from modelos.usuarios import Usuario
from nucleo.seguranca import verificar_senha
from nucleo.auth import criar_token
router = APIRouter(prefix="/auth", tags=["Auth"])


from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")

    if not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(status_code=400, detail="Senha inválida")

    token = criar_token({"sub": usuario.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }