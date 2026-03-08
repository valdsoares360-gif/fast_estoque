from pydantic import BaseModel, EmailStr


class UsuarioCriar(BaseModel):

    email: EmailStr
    senha: str


class UsuarioResposta(BaseModel):

    id: int
    email: str
    ativo: bool

    class Config:
        from_attributes = True