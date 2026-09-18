from typing import Optional

from sqlalchemy import CheckConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import MIN_FULL_AMOUNT, MIN_INVESTED_AMOUNT
from app.models.abstract_investment import AbstractInvestment


class Donation(AbstractInvestment):
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint(
            f"full_amount >= {MIN_FULL_AMOUNT}",
            name="ck_donation_full_amount_positive",
        ),
        CheckConstraint(
            f"invested_amount >= {MIN_INVESTED_AMOUNT}",
            name="ck_donation_invested_amount_non_negative",
        ),
        CheckConstraint(
            "invested_amount <= full_amount",
            name="ck_donation_invested_amount_lte_full_amount",
        ),
    )
