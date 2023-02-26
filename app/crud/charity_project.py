from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import label

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_charity_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == project_name)
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[dict[str, int]]:
        projects = await session.execute(
            select(
                [
                    CharityProject.name,
                    label(
                        "completion_rate",
                        (
                            func.unixepoch(CharityProject.close_date) -
                            func.unixepoch(CharityProject.create_date)
                        ),
                    ),
                    CharityProject.description,
                ]
            )
            .where(CharityProject.fully_invested.is_(True))
            .order_by("completion_rate")
        )
        projects = projects.all()
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
