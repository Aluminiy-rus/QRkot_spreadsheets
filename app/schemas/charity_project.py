from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None, title="название проекта", min_length=1, max_length=100
    )
    description: Optional[str] = Field(
        None,
        title="описание проекта",
        description="не менее одного символа",
        min_length=1,
    )
    full_amount: Optional[PositiveInt] = Field(
        None, title="требуемая сумма", description="больше 0"
    )


class CharityProjectCreate(CharityProjectBase):
    """Схема создания проекта пожертвований"""

    name: str = Field(..., title="название проекта", min_length=1, max_length=100)
    description: str = Field(..., title="описание проекта", min_length=1)
    full_amount: PositiveInt = Field(
        ..., title="требуемая сумма", description="больше 0"
    )


class CharityProjectUpdate(CharityProjectCreate):
    """Схема изменения проекта пожертвования"""

    name: str = Field(None, title="название проекта", min_length=1, max_length=100)
    description: str = Field(None, title="описание проекта", min_length=1)
    full_amount: PositiveInt = Field(
        None, title="требуемая сумма", description="больше 0"
    )

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    """Схема проекта пожертвования"""

    id: int
    invested_amount: Optional[int] = Field(
        title="внесённая сумма",
    )
    fully_invested: Optional[bool] = Field(
        title="собрана ли нужная сумма?",
    )
    create_date: Optional[datetime] = Field(
        title="дата создания проекта",
    )
    close_date: Optional[datetime] = Field(
        title="дата закрытия проекта",
    )

    class Config:
        orm_mode = True
