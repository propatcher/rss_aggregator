from sqlalchemy import delete,select
from app.database import async_session


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_by_id(cls, model_id: int):
        return await cls.find_one_or_none(id=model_id)

    @classmethod
    async def add(cls, **data):
        async with async_session() as session:
            instance = cls.model(**data)
            session.add(instance)
            await session.flush()
            await session.commit()
            return instance
    
    @classmethod
    async def delete(cls, **filter_by):
        async with async_session() as session:
            delete_query = delete(cls.model).filter_by(**filter_by)
            result = await session.execute(delete_query)
            await session.commit()
            return result.rowcount > 0
        
    @classmethod
    async def update_one(cls,new_data,**filter_by):
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