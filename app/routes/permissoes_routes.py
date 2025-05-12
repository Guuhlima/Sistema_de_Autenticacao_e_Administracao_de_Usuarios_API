from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi import Path
from app.database import SessionLocal
from app.models.permissoes import Permissao
from app.schemas.permissoes import PermissaoCreate, PermissaoRead

router = APIRouter(prefix="/permissoes", tags=["Permissões"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PermissaoRead, status_code=201)
def criar_permissao(dados: PermissaoCreate, db: Session = Depends(get_db)):

    existente = db.query(Permissao).filter_by(nome=dados.nome).first()
    if existente:
        raise HTTPException(status_code=400, detail="Permissão já existe")

    nova = Permissao(nome=dados.nome, descricao=dados.descricao)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

@router.get("/", response_model=list[PermissaoRead])
def listar_permissoes(db: Session = Depends(get_db)):
    return db.query(Permissao).all()

@router.delete("/{permissao_id}", status_code=204)
def deletar_permissao(
    permissao_id: int = Path(..., description="ID da permissão a ser removida"),
    db: Session = Depends(get_db)
):
    permissao = db.query(Permissao).filter(Permissao.id == permissao_id).first()

    if not permissao:
        raise HTTPException(status_code=404, detail="Permissão não encontrada")

    db.delete(permissao)
    db.commit()
    return