import abc
from datetime import datetime
from uuid import uuid4, UUID
from typing import Generic, TypeVar, Type
from fastapi import HTTPException

from sqlalchemy import func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import InstrumentedAttribute

from schemas.base import BaseSchema, BasePaginatedSchema

IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseSchema)
SCHEMA = TypeVar("SCHEMA", bound=BaseSchema)
PARTIAL_UPDATE_SCHEMA = TypeVar("PARTIAL_UPDATE_SCHEMA", bound=BaseSchema)
PAGINATED_SCHEMA = TypeVar("PAGINATED_SCHEMA", bound=BasePaginatedSchema)
TABLE = TypeVar("TABLE")


class BaseCrud(
    Generic[IN_SCHEMA, PARTIAL_UPDATE_SCHEMA, SCHEMA, PAGINATED_SCHEMA, TABLE],
    metaclass=abc.ABCMeta,
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
        entry_id = uuid4()
        now = datetime.now()
        entry = self._table(
            id=entry_id, created_at=now, modified_at=now, **in_schema.dict()
        )
        self._db_session.add(entry)
        await self._db_session.commit()
        return self._schema.from_orm(entry)

    async def get_by_id(self, entry_id: UUID) -> SCHEMA:
        entry = await self._db_session.get(self._table, entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Object not found")
        return self._schema.from_orm(entry)

    async def update_by_id(
        self, entry_id: UUID, in_data: PARTIAL_UPDATE_SCHEMA
    ) -> SCHEMA:
        entry = await self._db_session.get(self._table, entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Object not found")
        in_data_dict: dict = in_data.dict(exclude_unset=True)
        for _k, _v in in_data_dict.items():
            setattr(entry, _k, _v)
        await self._db_session.commit()
        return self._schema.from_orm(entry)

    async def delete_by_id(self, entry_id: UUID) -> None:
        entry = await self._db_session.get(self._table, entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Object not found")
        await self._db_session.delete(entry)
        return

    async def get_paginated_list(self, limit: int, offset: int) -> PAGINATED_SCHEMA:
        result: Result = await self._db_session.execute(
            select(self._table).order_by(self._order_by).limit(limit).offset(offset)
        )
        entries = result.scalars()
        total_count: Result = await self._db_session.execute(
            select(func.count()).select_from(self._table)
        )
        return self._paginated_schema(
            total=total_count.scalar(),
            items=[self._schema.from_orm(entry) for entry in entries],
        )
