from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationFullInfoDB
from app.services.investment import invest

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    "/",
    response_model=list[DonationFullInfoDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(session: SessionDep):
    return await donation_crud.get_all(session)


@router.get("/my", response_model=list[DonationDB])
async def get_all_donations(
    session: SessionDep, user: Annotated[User, Depends(current_user)]
):
    return await donation_crud.get_by_user(session, user)


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
    obj_in: DonationCreate,
    session: SessionDep,
    user: Annotated[User, Depends(current_user)],
):
    new_donation = await donation_crud.create(obj_in, session, user)
    sources = await charity_project_crud.get_uninvested(session)
    changed = invest(new_donation, sources)
    session.add_all(changed)
    await session.commit()
    return new_donation
