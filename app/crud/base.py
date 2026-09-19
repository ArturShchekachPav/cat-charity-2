from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User


class CRUDBase:
    def __init__(self, model: type[Base]):
        self.model = model

    async def create(
        self,
        obj_in: BaseModel,
        session: AsyncSession,
        user: Optional[User] = None,
    ):
        obj_in_data = obj_in.model_dump()
        if user is not None:
            obj_in_data["user_id"] = user.id
        new_obj = self.model(**obj_in_data)
        session.add(new_obj)
        await session.flush()
        return new_obj

    async def get_by_id(self, obj_id: int, session: AsyncSession):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_all(self, session: AsyncSession):
        db_objs = await session.execute(
            select(self.model).order_by(self.model.id)
        )
        return list(db_objs.scalars().all())

    async def update(
        self, db_obj: Base, obj_in: BaseModel, session: AsyncSession
    ):
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await session.flush()
        return db_obj

    async def remove(self, db_obj: Base, session: AsyncSession):
        await session.delete(db_obj)
        await session.flush()
        return db_obj


class CRUDInvestment(CRUDBase):
    async def get_uninvested(self, session: AsyncSession) -> list:
        db_objs = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )
        return list(db_objs.scalars().all())
