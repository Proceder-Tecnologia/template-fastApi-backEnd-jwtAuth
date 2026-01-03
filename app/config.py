from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = "mysql+aiomysql://root:password@localhost:3306/authdb"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # JWT
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # API
    api_v1_str: str = "/api/v1"
    project_name: str = "FastAPI JWT Auth Template"
    
    # Superuser for registration
    superuser_username: str = "admin"
    superuser_password: str = "admin123"
    admin_creation_token: str = "create-admin-secure-token-2024"
    
    class Config:
        env_file = ".env"

settings = Settings()