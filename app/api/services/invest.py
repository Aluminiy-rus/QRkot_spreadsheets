from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def status_check(
    session: AsyncSession,
):
    """Функция для получения приоритетного проекта и пожертвования"""
    all_opened_projects = await session.execute(
        select(CharityProject).where(CharityProject.fully_invested == 0)
    )
    priority_project = all_opened_projects.scalars().first()

    all_uninvested_donations = await session.execute(
        select(Donation).where(Donation.fully_invested == 0)
    )
    priority_donation = all_uninvested_donations.scalars().first()

    return priority_project, priority_donation


async def donation_func(session: AsyncSession, obj):
    """Функция для расчета пожертваваний"""
    project, donation = await status_check(session)

    if not project or not donation:
        await session.commit()
        await session.refresh(obj)
        return obj

    project_cash = project.full_amount - project.invested_amount
    donation_cash = donation.full_amount - donation.invested_amount

    if project_cash > donation_cash:
        project.invested_amount += donation_cash

        donation.invested_amount += donation_cash
        donation.fully_invested = True
        donation.close_date = datetime.now()

    elif project_cash == donation_cash:
        project.invested_amount += donation_cash
        project.fully_invested = True
        project.close_date = datetime.now()

        donation.invested_amount += donation_cash
        donation.fully_invested = True
        donation.close_date = datetime.now()

    else:
        donation.invested_amount += project_cash

        project.invested_amount += project_cash
        project.fully_invested = True
        project.close_date = datetime.now()

    session.add(project)
    session.add(donation)
    await session.commit()
    await session.refresh(project)
    await session.refresh(donation)
    return await donation_func(session, obj)
