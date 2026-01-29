from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.base_model import Base
import logging

logger = logging.getLogger(__name__)


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        self.db = db
        self.model = model

    async def get(self, id: int) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        query = select(self.model).offset(skip).limit(limit).order_by(self.model.id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.db.add(instance)
        try:
            await self.db.commit()
            await self.db.refresh(instance)
        except SQLAlchemyError as e:
            logger.error(e)
            await self.db.rollback()
            raise e
        return instance

    async def update(self, id: int, **kwargs) -> Optional[ModelType]:
        instance = await self.get(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            try:
                await self.db.commit()
            except SQLAlchemyError as e:
                logger.error(f"Error updating {self.model.__name__} with {kwargs}: {e}")
                await self.db.rollback()
                raise e
        return instance

    async def delete(self, id: int) -> bool:
        instance = await self.get(id)

        if not instance:
            logger.warning(f"Attempted to delete non-existent {self.model.__name__} with id {id}")
            return False
        try:
            await self.db.delete(instance)
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error deleting {self.model.__name__}: {e}")
            await self.db.rollback()
            raise e
