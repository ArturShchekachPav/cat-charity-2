from app.crud.base import CRUDInvestment
from app.models.donation import Donation
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User


class CRUDDonation(CRUDInvestment):
    async def get_by_user(
            self, session: AsyncSession, user: User
    ):
        donations = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
