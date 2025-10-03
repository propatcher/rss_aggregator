from sqlalchemy import or_, select
from app.DAO.base_dao import BaseDAO
from app.User.models import User
from app.database import async_session

class UserDAO(BaseDAO):
    model = User
    
    async def find_by_email_or_username(identifier: str):
        async with async_session() as session:
            query = select(User).where(
                or_(User.email == identifier, User.username == identifier)
                )
            result = await session.execute(query)
            return result.scalars().one_or_none()