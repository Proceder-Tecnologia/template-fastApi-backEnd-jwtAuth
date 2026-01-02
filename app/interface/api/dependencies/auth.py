from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from app.infrastructure.database.connection import get_session
from app.infrastructure.database.repositories.user_repository import SQLUserRepository
from app.infrastructure.security.jwt_service import SecurityService
from app.infrastructure.cache.redis_service import RedisService
from app.application.services.auth_service import AuthService

security = HTTPBearer()

def get_user_repository(session: AsyncSession = Depends(get_session)) -> SQLUserRepository:
    return SQLUserRepository(session)

def get_auth_service(user_repository: SQLUserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository)

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> str:
    token = credentials.credentials
    
    # Verificar se o token está na blacklist
    if RedisService.is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = SecurityService.verify_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_id