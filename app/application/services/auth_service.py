from datetime import datetime
from typing import Optional
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.security.jwt_service import SecurityService
from app.infrastructure.cache.redis_service import RedisService
from app.interface.schemas.auth import UserCreate, UserLogin, Token, UserResponse
from app.interface.schemas.admin import AdminCreate
from app.config import settings

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.security_service = SecurityService()
        self.redis_service = RedisService()
    
    async def create_admin(self, admin_data: AdminCreate) -> UserResponse:
        # Verificar token de admin
        if admin_data.admin_token != settings.admin_creation_token:
            raise ValueError("Invalid admin creation token")
        
        # Verificar se usuário já existe
        existing_user = await self.user_repository.get_by_email(admin_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = await self.user_repository.get_by_username(admin_data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        # Criar novo admin
        hashed_password = self.security_service.get_password_hash(admin_data.password)
        user = User(
            email=admin_data.email,
            username=admin_data.username,
            firstname=admin_data.firstname,
            lastname=admin_data.lastname,
            hashed_password=hashed_password,
            is_superuser=True
        )
        
        created_user = await self.user_repository.create(user)
        return UserResponse(**created_user.dict())
    
    async def register(self, user_data: UserCreate) -> UserResponse:
        # Verificar se usuário já existe
        existing_user = await self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = await self.user_repository.get_by_username(user_data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        # Criar novo usuário
        hashed_password = self.security_service.get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            hashed_password=hashed_password,
            is_superuser=False
        )
        
        created_user = await self.user_repository.create(user)
        return UserResponse(**created_user.dict())
    
    async def login(self, login_data: UserLogin) -> Token:
        user = await self.user_repository.get_by_email(login_data.email)
        if not user or not self.security_service.verify_password(login_data.password, user.hashed_password):
            raise ValueError("Invalid credentials")
        
        if not user.is_active:
            raise ValueError("User account is disabled")
        
        # Atualizar last_login
        user.last_login = datetime.utcnow()
        await self.user_repository.update(user)
        
        # Gerar tokens
        access_token = self.security_service.create_access_token(data={"sub": user.id})
        refresh_token = self.security_service.create_refresh_token(data={"sub": user.id})
        
        # Salvar refresh token no Redis
        self.redis_service.set_refresh_token(user.id, refresh_token)
        
        return Token(access_token=access_token, refresh_token=refresh_token)
    
    async def refresh_token(self, refresh_token: str) -> Token:
        user_id = self.security_service.verify_token(refresh_token, "refresh")
        if not user_id:
            raise ValueError("Invalid refresh token")
        
        # Verificar se o refresh token está no Redis
        stored_token = self.redis_service.get_refresh_token(user_id)
        if not stored_token or stored_token != refresh_token:
            raise ValueError("Invalid refresh token")
        
        user = await self.user_repository.get_by_id(user_id)
        if not user or not user.is_active:
            raise ValueError("User not found or inactive")
        
        # Gerar novos tokens
        new_access_token = self.security_service.create_access_token(data={"sub": user.id})
        new_refresh_token = self.security_service.create_refresh_token(data={"sub": user.id})
        
        # Atualizar refresh token no Redis
        self.redis_service.set_refresh_token(user.id, new_refresh_token)
        
        return Token(access_token=new_access_token, refresh_token=new_refresh_token)
    
    async def logout(self, access_token: str, user_id: str):
        # Remover refresh token do Redis
        self.redis_service.delete_refresh_token(user_id)
        
        # Adicionar access token à blacklist
        self.redis_service.blacklist_token(access_token, 30 * 60)  # 30 minutos
    
    async def get_current_user(self, user_id: str) -> Optional[UserResponse]:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            return None
        return UserResponse(**user.dict())