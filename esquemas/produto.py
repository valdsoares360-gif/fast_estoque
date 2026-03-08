from pydantic import BaseModel


class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    preco: float
    quantidade: int
    estoque_minimo: int


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        orm_mode = True



class MovimentacaoCreate(BaseModel):
    produto_id: int
    tipo: str
    quantidade: int