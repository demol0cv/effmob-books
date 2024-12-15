import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=lambda: datetime.datetime.now(tz=datetime.UTC).replace(tzinfo=None))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        onupdate=lambda: datetime.datetime.now(tz=datetime.UTC).replace(tzinfo=None),
        default=lambda: datetime.datetime.now(tz=datetime.UTC).replace(tzinfo=None),
        )
