from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.interface.api.routes import auth
from app.interface.api.lifespan import lifespan
from app.config import settings

app = FastAPI(
    title=settings.project_name,
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    lifespan=lifespan
)

# CORS dinâmico baseado no ambiente
if settings.environment == "production":
    # Produção: Origins específicos
    cors_origins = ["https://yourdomain.com"]  # Substitua pelo seu domínio
else:
    # Desenvolvimento: Localhost
    cors_origins = settings.cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,  # CRÍTICO: Permite cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(auth.router, prefix=settings.api_v1_str)

@app.get("/")
def read_root():
    return {"message": "FastAPI JWT Auth Template is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}