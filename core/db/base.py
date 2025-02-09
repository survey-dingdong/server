from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

if TYPE_CHECKING:
    from sqlalchemy.sql.schema import ColumnCollectionConstraint, Table


class Base(MappedAsDataclass, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        init=False,
        index=True,
    )

    updated_at: Mapped[datetime.datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        onupdate=lambda: datetime.datetime.now(datetime.UTC),
        nullable=True,
        init=False,
    )


class BaseWithInId(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )


def _table_guid_generator(
    constraint: ColumnCollectionConstraint,
    table: Table,
) -> str:
    str_tokens = [table.name] + [col.name for col in constraint.columns]
    if constraint.info is not None and "extra_guid_token" in constraint.info:
        str_tokens.append(constraint.info["extra_guid_token"])
    guid = uuid.uuid5(uuid.NAMESPACE_OID, "_".join(str_tokens))
    return guid.hex


Base.metadata.naming_convention = {
    "guid": _table_guid_generator,  # type: ignore
    "pk": "pk_%(table_name)s",
    "ix": "ix_%(guid)s",
    "uq": "uq_%(guid)s",
    "fk": "fk_%(guid)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
}
