from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
from datetime import datetime
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository

class SQLUserRepository(UserRepository):
    async def create(self, session: AsyncSession, user: User) -> User:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()
    
    async def get_by_username(self, session: AsyncSession, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        return result.first()
    
    async def get_by_id(self, session: AsyncSession, user_id: str) -> Optional[User]:
        statement = select(User).where(User.id == user_id)
        result = await session.exec(statement)
        return result.first()
    
    async def update(self, session: AsyncSession, user: User) -> User:
        user.updated_at = datetime.utcnow()
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user