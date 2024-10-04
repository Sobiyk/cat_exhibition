from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.crud.breed import breed_crud
from app.models.cat import Breed, Cat
from app.schemas.cat import CatCreate


class CatCRUD(CRUDBase):

    async def get_multi_filter_by_breed(
        self,
        breed: str,
        session: AsyncSession,
    ):
        if breed is None:
            return await self.get_multi(session)
        all_objects = await session.execute(
            select(self.model)
            .join(Breed, self.model.breed_id == Breed.id)
            .where(Breed.name.in_(breed))
        )
        return all_objects.unique().scalars().all()

    async def create(
        self,
        cat_in: CatCreate,
        session: AsyncSession
    ):
        obj_in_data = cat_in.model_dump(exclude_none=True)
        breed_name = obj_in_data.pop('breed')
        breed_id = await breed_crud.get_id_by_name(
            breed_name, session
        )
        obj_in_data['breed_id'] = breed_id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, update_data, db_obj, session: AsyncSession):
        obj_data = jsonable_encoder(db_obj)
        update_dict = update_data.model_dump(exclude_none=True)
        breed_name = update_dict.pop('breed', None)
        if breed_name is not None:
            breed_id = await breed_crud.get_id_by_name(breed_name, session)
            update_dict['breed_id'] = breed_id
        for field in obj_data:
            if field in update_dict:
                setattr(db_obj, field, update_dict[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


cat_crud = CatCRUD(Cat)
