from fastapi import Depends, HTTPException, status, Request
from app.infrastructure.security.jwt_service import SecurityService
from app.infrastructure.cache.redis_service import RedisService

async def get_current_user_id_from_cookie(request: Request) -> str:
    access_token = request.cookies.get("access_token")
    
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token not found",
        )
    
    # Verificar se o token está na blacklist
    if RedisService.is_token_blacklisted(access_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
        )
    
    user_id = SecurityService.verify_token(access_token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    return user_id