from pydantic import BaseModel


class MovimentacaoCreate(BaseModel):
    produto_id: int
    tipo: str
    quantidade: int