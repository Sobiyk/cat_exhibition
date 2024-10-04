from typing_extensions import Annotated, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.breed import Breed
from app.core.db import Base

intpk = Annotated[int, mapped_column(primary_key=True)]


class Cat(Base):
    """Модель кошечек."""
    name: Mapped[Optional[str]]
    color: Mapped[str]
    age: Mapped[int]
    description: Mapped[str]
    breed_id: Mapped[int] = mapped_column(ForeignKey('breed.id'))
    breed = relationship(Breed, lazy='joined')
