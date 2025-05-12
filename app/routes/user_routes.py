from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.models.usuarios import Usuario
from app.models.logs import Log
from app.models.usuario_permissoes import UsuarioPermissao
from app.schemas.usuarios import UsuarioCreate, UsuarioLogin, UsuarioOut, Token
from app.utils.security import gerar_hash_senha, verificar_senha, criar_token_acesso

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST
@router.post("/register")
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(models.Usuario).filter_by(email=usuario.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=gerar_hash_senha(usuario.senha),
        status="ativo"
    )
    db.add(novo_usuario)
    db.commit()
    return {"mensagem": "Usuário cadastrado com sucesso"}

@router.post("/login", response_model=Token)
def login(usuario: UsuarioLogin, request: Request, db: Session = Depends(get_db)):
    user = db.query(models.Usuario).filter_by(email=usuario.email).first()
    ip = request.client.host

    if not user or not verificar_senha(usuario.senha, user.senha_hash):
        log = Log(tipo_evento="login_falha", ip_origem=ip)
        if user:
            log.usuario_id = user.id
        db.add(log)
        db.commit()
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    log = Log(tipo_evento="login_sucesso", usuario_id=user.id, ip_origem=ip)
    db.add(log)
    db.commit()
    
    access_token = criar_token_acesso({"sub": user.email})

    return {
        "mensagem": f"Login bem-sucedido para {user.nome}",
        "access_token": access_token,
        "token_type": "bearer",
        "id": user.id
    }

@router.post("/usuarios/{usuario_id}/permissoes")
def atribuir_permissao(usuario_id: int, permissao_id: int, db: Session = Depends(get_db)):

    usuario = db.query(models.Usuario).filter_by(id=usuario_id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    relacao = UsuarioPermissao(usuario_id=usuario_id, permissao_id=permissao_id)
    db.add(relacao)
    db.commit()

    permissao = db.query(models.Permissao).filter_by(id=permissao_id).first()

    return {
        "mensagem": "Permissão atribuída com sucesso",
        "usuario_nome": usuario.nome,
        "permissao_nome": permissao.nome if permissao else "Permissão não encontrada"
    }
    
# GET
@router.get("/usuarios", response_model=list[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.get("/usuarios/{usuario_id}/permissoes")
def obter_permissoes_do_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(id=usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    permissoes = db.query(UsuarioPermissao).filter_by(usuario_id=usuario_id).all()

    if not permissoes:
        return {"mensagem": "Usuário não possui permissões atribuídas.", "permissoes": []}

    return {
        "usuario_id": usuario_id,
        "permissoes": [p.permissao_id for p in permissoes]
    }

# DELETE
@router.delete("/usuarios/{usuario_id}/permissoes/{permissao_id}")
def remover_permissao(usuario_id: int, permissao_id: int, db: Session = Depends(get_db)):
    relacao = db.query(UsuarioPermissao).filter_by(usuario_id=usuario_id, permissao_id=permissao_id).first()

    if not relacao:
        raise HTTPException(status_code=404, detail="Permissão não atribuída a este usuário.")

    db.delete(relacao)
    db.commit()

    return {"mensagem": "Permissão removida com sucesso."}

@router.delete("/usuarios/{usuario_id}", response_model=UsuarioOut)
def excluir_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(id=usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    db.delete(usuario)
    db.commit()

    log = Log(tipo_evento="excluir_conta", usuario_id=usuario_id, ip_origem="127.0.0.1")
    db.add(log)
    db.commit()

    return usuario