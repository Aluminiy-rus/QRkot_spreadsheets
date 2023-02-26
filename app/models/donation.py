from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.extended_base import ExtendedBase


class Donation(ExtendedBase):
    user_id = Column(Integer, ForeignKey("user.id", name="fk_donation_user_id_user"))
    comment = Column(Text, nullable=True)
