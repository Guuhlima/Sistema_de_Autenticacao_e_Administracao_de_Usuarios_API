from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes.user_routes import router as user_router
from app.routes.permissoes_routes import router as permissoes_router
from app.routes.logs_routes import router as logs_router
from app.routes.password_routes import router as senha_router

app = FastAPI(title="APIs de Login e Permissões")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/auth", tags=["Autenticação"])
app.include_router(permissoes_router)
app.include_router(logs_router)
app.include_router(senha_router)
