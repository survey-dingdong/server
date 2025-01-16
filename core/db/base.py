import datetime

from sqlalchemy import TIMESTAMP, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class Base(MappedAsDataclass, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP,
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        init=False,
        index=True,
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP,
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc),
        init=False,
    )


class BaseWithInId(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )
