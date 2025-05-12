from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.logs import Log
from app.schemas.logs import LogRead 

router = APIRouter(prefix="/logs", tags=["Logs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[LogRead])
def listar_todos_logs(db: Session = Depends(get_db)):
    logs = db.query(Log).all()
    return logs

@router.get("/{usuario_id}", response_model=list[LogRead])
def obter_logs(usuario_id: int, db: Session = Depends(get_db)):
    logs = db.query(Log).filter_by(usuario_id=usuario_id).all()
    
    if not logs:
        raise HTTPException(status_code=404, detail="Nenhum log encontrado para esse usuário")

    return logs
