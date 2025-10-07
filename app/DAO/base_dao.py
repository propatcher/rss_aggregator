from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session
from app.logger import logger


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):   #TODO Больше обработок exception
        try:
            async with async_session() as session:
                query = select(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                return result.scalars().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
                msg += ": Cannot find one or none"
            else:
                msg = f"Unexpected Exception ({type(e).__name__})"                
            extra = {"model": cls, "filters": filter_by}
            logger.error(msg, extra=extra)
            raise

    @classmethod
    async def find_all(cls, **filter_by):
        try:
            async with async_session() as session:
                query = select(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                return result.scalars().all()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
                msg += ": Cannot find all"
            else:
                msg = f"Unexpected Exception ({type(e).__name__})"                
            extra = {"model": cls, "filters": filter_by}
            logger.error(msg, extra=extra)
            raise

    @classmethod
    async def find_by_id(cls, model_id: int):
        try:
            return await cls.find_one_or_none(id=model_id)
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
                msg += ": Cannot find one or none"
            else:
                msg = f"Unexpected Exception ({type(e).__name__})"                
            extra = {"model": cls, "model_id": model_id}
            logger.error(msg, extra=extra)
            raise

    @classmethod
    async def add(cls, **data):
        try:
            async with async_session() as session:
                instance = cls.model(**data)
                session.add(instance)
                await session.flush()
                await session.commit()
            return instance
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
                msg += ": Cannot find one or none"
            else:
                msg = f"Unexpected Exception ({type(e).__name__})"                
            extra = {"model": cls, "data": data}
            logger.error(msg, extra=extra)
            raise

    @classmethod
    async def delete(cls, **filter_by):
        try:
            async with async_session() as session:
                delete_query = delete(cls.model).filter_by(**filter_by)
                result = await session.execute(delete_query)
                await session.commit()
                return result.rowcount > 0
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
                msg += ": Cannot find one or none"
            else:
                msg = f"Unexpected Exception ({type(e).__name__})"                
            extra = {"model": cls, "filters": filter_by}
            logger.error(msg, extra=extra)
            raise

    @classmethod
    async def update_one(cls, new_data, **filter_by):
        try:
            async with async_session() as session:
                query = select(cls.model).filter_by(**filter_by).limit(1)
                result = await session.execute(query)
                instance = result.scalar_one_or_none()

                if not instance:
                    return None

                for key, value in new_data.items():
                    setattr(instance, key, value)

                await session.commit()
                return instance
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
                msg += ": Cannot find one or none"
            else:
                msg = f"Unexpected Exception ({type(e).__name__})"                
            extra = {"model": cls, "filters": filter_by}
            logger.error(msg, extra=extra)
            raise
