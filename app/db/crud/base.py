import abc
from typing import Generic, TypeVar, Type
from uuid import uuid4, UUID

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import InstrumentedAttribute

from db.errors import DoesNotExist
from schemas.base import BaseSchema, BasePaginatedSchema

IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseSchema)
SCHEMA = TypeVar("SCHEMA", bound=BaseSchema)
PAGINATED_SCHEMA = TypeVar("PAGINATED_SCHEMA", bound=BasePaginatedSchema)
TABLE = TypeVar("TABLE")


class BaseCrud(
    Generic[IN_SCHEMA, SCHEMA, PAGINATED_SCHEMA, TABLE], metaclass=abc.ABCMeta
):
    def __init__(self, db_session: AsyncSession, *args, **kwargs) -> None:
        self._db_session: AsyncSession = db_session

    @property
    @abc.abstractmethod
    def _table(self) -> Type[TABLE]:
        ...

    @property
    @abc.abstractmethod
    def _schema(self) -> Type[SCHEMA]:
        ...

    @property
    @abc.abstractmethod
    def _order_by(self) -> InstrumentedAttribute:
        ...

    @property
    @abc.abstractmethod
    def _paginated_schema(self) -> Type[PAGINATED_SCHEMA]:
        ...

    async def create(self, in_schema: IN_SCHEMA) -> SCHEMA:
        entry = self._table(id=uuid4(), **in_schema.dict())
        self._db_session.add(entry)
        await self._db_session.commit()
        return self._schema.from_orm(entry)

    async def get_by_id(self, entry_id: UUID) -> SCHEMA:
        entry = await self._db_session.get(self._table, entry_id)
        if not entry:
            raise DoesNotExist(f"{self._table.__name__}<id:{entry_id}> does not exist")
        return self._schema.from_orm(entry)

    async def get_paginated_list(self, limit: int, offset: int) -> PAGINATED_SCHEMA:
        entries = await self._db_session.execute(  # todo: this won't work, refactor
            select(self._table).order_by(self._order_by).limit(limit).offset(offset)
        )
        total_count = await self._db_session.execute(  # todo: this won't work, refactor
            select(func.count()).select_from(self._table)
        )
        return self._paginated_schema(total=total_count, items=list(entries))
