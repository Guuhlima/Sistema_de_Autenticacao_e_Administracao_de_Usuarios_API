from pydantic import BaseModel
from datetime import datetime 

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioLogin(BaseModel):
    email: str
    senha: str

class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str
    status: str
    data_criacao: datetime

class Token(BaseModel):
    mensagem: str
    access_token: str
    token_type: str = "bearer"
    id: int