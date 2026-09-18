from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators.charity_project import (
    check_charity_project_exists,
    check_charity_project_name_duplicate,
    check_charity_project_updated_full_amount_not_less_invested,
    check_charity_project_updated_name_duplicate,
    check_project_has_no_investments,
    check_project_is_open,
)
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import close_if_fully_invested, invest

router = APIRouter(prefix="/charity_project", tags=["charity_projects"])

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get("/", response_model=list[CharityProjectDB])
async def get_all_charity_projects(session: SessionDep):
    return await charity_project_crud.get_all(session)


@router.post("/", response_model=CharityProjectDB)
async def create_new_charity_project(
    obj_in: CharityProjectCreate, session: SessionDep
):
    await check_charity_project_name_duplicate(obj_in.name, session)
    new_project = await charity_project_crud.create(obj_in, session)
    sources = await donation_crud.get_uninvested(session)
    changed = invest(new_project, sources)
    session.add_all(changed)
    await session.commit()
    return new_project


@router.patch("/{project_id}", response_model=CharityProjectDB)
async def partiallyupdate_charity_project(
    project_id: int, obj_in: CharityProjectUpdate, session: SessionDep
):
    charity_project = await check_charity_project_exists(project_id, session)
    check_project_is_open(charity_project)
    await check_charity_project_updated_name_duplicate(
        charity_project, obj_in, session
    )
    check_charity_project_updated_full_amount_not_less_invested(
        charity_project, obj_in
    )
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    close_if_fully_invested(charity_project)
    await session.commit()
    return charity_project


@router.delete("/{project_id}", response_model=CharityProjectDB)
async def remove_charity_project(
    project_id: int,
    session: SessionDep,
):
    charity_project = await check_charity_project_exists(project_id, session)
    check_project_has_no_investments(charity_project)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    await session.commit()
    return charity_project
