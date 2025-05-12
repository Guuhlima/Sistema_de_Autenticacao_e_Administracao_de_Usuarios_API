from pydantic import BaseModel

class PermissaoCreate(BaseModel):
    nome: str
    descricao: str

class PermissaoRead(BaseModel):
    id: int
    nome: str
    descricao: str

    class Config:
        orm_mode = True