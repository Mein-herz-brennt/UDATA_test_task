from typing import Generic, TypeVar, List, Optional, Any, Sequence
from app.repositories.base_repository import BaseRepository, ModelType

RepoType = TypeVar("RepoType", bound=BaseRepository)


class BaseService(Generic[ModelType, RepoType]):
    def __init__(self, repository: RepoType):
        self.repository = repository

    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        return await self.repository.get(id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return await self.repository.get_all(skip=skip, limit=limit)

    async def create(self, **data) -> ModelType:
        return await self.repository.create(**data)

    async def update(self, id: Any, **data) -> Optional[ModelType]:
        return await self.repository.update(id, **data)

    async def delete(self, id: Any) -> bool:
        return await self.repository.delete(id)