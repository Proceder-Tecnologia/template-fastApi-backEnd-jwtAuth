from abc import ABC, abstractmethod
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from app.domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    async def create(self, session: AsyncSession, user: User) -> User:
        pass
    
    @abstractmethod
    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_by_username(self, session: AsyncSession, username: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_by_id(self, session: AsyncSession, user_id: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def update(self, session: AsyncSession, user: User) -> User:
        pass