from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from banco.db import get_db
from modelos.usuarios import Usuario

SECRET_KEY = "segredo_super_seguro"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def criar_token(dados: dict):
    dados_para_codificar = dados.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    dados_para_codificar.update({"exp": expire})

    token = jwt.encode(dados_para_codificar, SECRET_KEY, algorithm=ALGORITHM)

    return token

def get_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    credenciais_exception = HTTPException(
        status_code=401,
        detail="Credenciais inválidas"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credenciais_exception

    except JWTError:
        raise credenciais_exception

    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if usuario is None:
        raise credenciais_exception

    return usuario