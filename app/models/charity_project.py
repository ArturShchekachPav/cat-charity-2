from sqlalchemy import CheckConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import (
    DESCRIPTION_MIN_LENGTH,
    MIN_FULL_AMOUNT,
    MIN_INVESTED_AMOUNT,
    NAME_MAX_LENGTH,
    NAME_MIN_LENGTH,
)
from app.models.abstract_investment import AbstractInvestment


class CharityProject(AbstractInvestment):
    name: Mapped[str] = mapped_column(
        String(NAME_MAX_LENGTH), unique=True, nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (
        CheckConstraint(
            f"length(name) >= {NAME_MIN_LENGTH}",
            name="ck_project_name_min_length",
        ),
        CheckConstraint(
            f"length(description) >= {DESCRIPTION_MIN_LENGTH}",
            name="ck_project_description_min_length",
        ),
        CheckConstraint(
            f"full_amount >= {MIN_FULL_AMOUNT}",
            name="ck_project_full_amount_positive",
        ),
        CheckConstraint(
            f"invested_amount >= {MIN_INVESTED_AMOUNT}",
            name="ck_project_invested_amount_non_negative",
        ),
        CheckConstraint(
            "invested_amount <= full_amount",
            name="ck_project_invested_amount_lte_full_amount",
        ),
    )
