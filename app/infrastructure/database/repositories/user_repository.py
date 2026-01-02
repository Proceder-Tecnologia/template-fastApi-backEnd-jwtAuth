from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
from datetime import datetime
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository

class SQLUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = await self.session.exec(statement)
        return result.first()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        result = await self.session.exec(statement)
        return result.first()
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        statement = select(User).where(User.id == user_id)
        result = await self.session.exec(statement)
        return result.first()
    
    async def update(self, user: User) -> User:
        user.updated_at = datetime.utcnow()
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user