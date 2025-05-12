from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "sua_chave_secreta"  # Troque depois por uma mais segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha, hash):
    return pwd_context.verify(senha, hash)

def gerar_hash_senha(senha):
    return pwd_context.hash(senha)

def criar_token_acesso(dados: dict):
    to_encode = dados.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
