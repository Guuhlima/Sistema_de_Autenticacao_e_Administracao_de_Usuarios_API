import secrets
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.usuarios import Usuario
from app.models.tokens import Token
from app.schemas.tokens import RecuperarSenhaRequest, RedefinirSenhaRequest
from app.utils.security import gerar_hash_senha
from datetime import datetime

router = APIRouter(prefix="/senha", tags=["Recuperação de Senha"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/recuperar")
def solicitar_recuperacao_senha(request: RecuperarSenhaRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == request.email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="E-mail não encontrado.")

    token = secrets.token_hex(16)

    novo_token = Token(usuario_id=usuario.id, token=token)
    db.add(novo_token)
    db.commit()

    return {"mensagem": "Token de recuperação gerado com sucesso.", "token": token}

@router.post("/redefinir")
def redefinir_senha(request: RedefinirSenhaRequest, db: Session = Depends(get_db)):
    token_entry = db.query(Token).filter(Token.token == request.token).first()

    if not token_entry or token_entry.data_expiracao < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token inválido ou expirado.")

    usuario = db.query(Usuario).filter(Usuario.id == token_entry.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    usuario.senha_hash = gerar_hash_senha(request.nova_senha)
    db.delete(token_entry)
    db.commit()

    return {"mensagem": "Senha redefinida com sucesso!"}
