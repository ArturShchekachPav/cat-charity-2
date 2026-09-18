from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin
from app.core.utils import get_utc_now


class AbstractInvestment(CommonMixin, Base):
    __abstract__ = True

    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    invested_amount: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=get_utc_now,
    )
    close_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )
