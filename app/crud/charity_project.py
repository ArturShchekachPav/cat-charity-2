from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDInvestment
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDInvestment):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(self.model.id).where(self.model.name == project_name)
        )
        return db_project_id.scalars().first()


charity_project_crud = CRUDCharityProject(CharityProject)
