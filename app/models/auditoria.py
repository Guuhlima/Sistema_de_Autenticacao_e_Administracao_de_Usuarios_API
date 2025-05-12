from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class Auditoria(Base):
    __tablename__ = "auditoria"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    campo_modificado = Column(String)
    valor_anterior = Column(String)
    valor_novo = Column(String)
    data_modificacao = Column(DateTime, default=datetime.utcnow)
