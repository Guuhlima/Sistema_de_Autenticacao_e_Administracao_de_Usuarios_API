from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class UsuarioPermissao(Base):
    __tablename__ = 'usuario_permissoes'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    permissao_id = Column(Integer, ForeignKey('permissoes.id'))
