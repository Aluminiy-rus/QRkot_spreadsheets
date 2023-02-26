from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationCreate(BaseModel):
    """Схема создания пожертвования"""

    full_amount: PositiveInt = Field(
        title="сумма пожертвования", description="больше 0"
    )
    comment: Optional[str] = Field(
        title="комментарий", description="необязательное текстовое поле"
    )


class DonationDB(DonationCreate):
    """Схема пожертвования"""

    id: int
    user_id: Optional[int] = Field(
        title="id пользователя, сделавшего пожертвование",
    )
    invested_amount: Optional[int] = Field(
        title="сумма из пожертвования, которая распределена по проектам",
    )
    fully_invested: Optional[bool] = Field(
        title="все ли деньги из пожертвования были переведены в тот или иной проект",
    )
    create_date: Optional[datetime] = Field(
        title="дата пожертвования",
    )
    close_date: Optional[datetime] = Field(
        title="дата, когда вся сумма пожертвования была распределена по проектам",
    )

    class Config:
        orm_mode = True
