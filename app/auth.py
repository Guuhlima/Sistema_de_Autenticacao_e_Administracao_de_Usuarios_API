from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from .database import SessionLocal
from .models import Usuario
from .utils.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_usuario(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        db = SessionLocal()
        usuario = db.query(Usuario).filter(Usuario.email == email).first()
        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
