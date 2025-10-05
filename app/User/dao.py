from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.DAO.base_dao import BaseDAO
from app.database import async_session
from app.logger import logger
from app.User.models import User


class UserDAO(BaseDAO):
    model = User

    async def find_by_email_or_username(identifier: str):
        try:
            async with async_session() as session:
                query = select(User).where(
                    or_(User.email == identifier, User.username == identifier)
                )
                result = await session.execute(query)
                return result.scalars().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
                msg += ": Cannot add feed"
            else:
                msg = f"Unexpected Exception ({type(e).__name__})"
            extra = {
                "identifier": identifier,
            }
            logger.error(msg, extra=extra)
            raise
