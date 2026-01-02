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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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