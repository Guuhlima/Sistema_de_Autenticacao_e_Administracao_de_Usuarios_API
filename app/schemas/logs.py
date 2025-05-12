from pydantic import BaseModel
from datetime import datetime

class LogRead(BaseModel):
    id: int
    usuario_id: int | None
    tipo_evento: str
    data_evento: datetime
    ip_origem: str

    class Config:
        orm_mode = True
