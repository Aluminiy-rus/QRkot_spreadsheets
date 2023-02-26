from sqlalchemy import Column, String, Text

from app.models.extended_base import ExtendedBase


class CharityProject(ExtendedBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
