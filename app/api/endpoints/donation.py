from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.services.invest import donation_func
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB

router = APIRouter()


@router.get(
    "/",
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude={"close_date"},
)
async def get_all_donations(session: AsyncSession = Depends(get_async_session)):
    """
    Только для суперюзеров.

    Получает список всех пожертвований.
    """
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={
        "close_date",
        "fully_invested",
        "invested_amount",
        "user_id",
    },
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Сделать пожертвование.
    """
    donation = await donation_crud.create(donation, session, user)
    donation = await donation_func(session, donation)
    return donation


@router.get(
    "/my",
    response_model=list[DonationDB],
    response_model_exclude={
        "user_id",
        "close_date",
        "fully_invested",
        "invested_amount",
    },
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получить список моих пожертвований."""
    donations = await donation_crud.get_by_user(session=session, user=user)
    return donations
