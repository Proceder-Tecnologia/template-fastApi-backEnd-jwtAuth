from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBasicCredentials
from app.interface.schemas.auth import UserCreate, UserLogin, LoginResponse, RefreshToken, UserResponse
from app.interface.schemas.admin import AdminCreate
from app.interface.api.dependencies.auth import get_auth_service, get_current_user_id, security
from app.interface.api.dependencies.superuser import verify_superuser_credentials
from app.interface.api.dependencies.permissions import verify_superuser
from app.interface.api.dependencies.cookies import get_current_user_id_from_cookie
from app.application.services.auth_service import AuthService
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/create-admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_admin(
    admin_data: AdminCreate,
    auth_service: AuthService = Depends(get_auth_service),
    credentials: HTTPBasicCredentials = Depends(verify_superuser_credentials)
):
    try:
        return await auth_service.create_admin(admin_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/create-user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
    current_user_id: str = Depends(get_current_user_id_from_cookie)
):
    try:
        return await auth_service.register(user_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=LoginResponse)
async def login(
    response: Response,
    login_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        user, access_token, refresh_token = await auth_service.login(login_data)
        
        # Configurar cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=settings.access_token_expire_minutes * 60,
            httponly=settings.cookie_httponly,
            secure=settings.cookie_secure,
            samesite=settings.cookie_samesite
        )
        
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
            httponly=settings.cookie_httponly,
            secure=settings.cookie_secure,
            samesite=settings.cookie_samesite
        )
        
        return LoginResponse(user=user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/refresh", response_model=dict)
async def refresh_token(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise ValueError("Refresh token not found")
        
        new_access_token, new_refresh_token = await auth_service.refresh_token(refresh_token)
        
        # Atualizar cookies
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            max_age=settings.access_token_expire_minutes * 60,
            httponly=settings.cookie_httponly,
            secure=settings.cookie_secure,
            samesite=settings.cookie_samesite
        )
        
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
            httponly=settings.cookie_httponly,
            secure=settings.cookie_secure,
            samesite=settings.cookie_samesite
        )
        
        return {"message": "Tokens refreshed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    response: Response,
    user_id: str = Depends(get_current_user_id_from_cookie),
    auth_service: AuthService = Depends(get_auth_service)
):
    access_token = request.cookies.get("access_token")
    if access_token:
        await auth_service.logout(access_token, user_id)
    
    # Remover cookies
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: str = Depends(get_current_user_id_from_cookie),
    auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.get_current_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user