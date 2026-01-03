from fastapi import Depends, HTTPException, status
from app.interface.api.dependencies.auth import get_current_user_id, get_auth_service
from app.application.services.auth_service import AuthService

async def verify_superuser(
    user_id: str = Depends(get_current_user_id),
    auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.get_current_user(user_id)
    if not user or not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return user_id