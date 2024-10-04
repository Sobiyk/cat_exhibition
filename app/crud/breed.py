from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.exceptions.crud.cat import BreedNotFoundException
from app.models.cat import Breed


class BreedCRUD(CRUDBase):

    async def get_id_by_name(self, name, session: AsyncSession):
        breed_id = await session.execute(
            select(Breed.id).where(Breed.name == name)
        )
        breed_id = breed_id.scalar()
        if breed_id is None:
            raise BreedNotFoundException(name)
        return breed_id


breed_crud = BreedCRUD(Breed)
