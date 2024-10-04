from sqlalchemy.orm import Mapped

from app.core.db import Base


class Breed(Base):
    """Модель породы."""
    name: Mapped[str]
