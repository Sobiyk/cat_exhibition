from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.crud.base import ObjectIDNotFoundException


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession):
        db_obj = await session.execute(
            select(self.model)
            .where(self.model.id == obj_id)
        )
        obj = db_obj.scalars().first()
        if obj is None:
            raise ObjectIDNotFoundException(obj_id)
        return obj

    async def get_multi(self, session: AsyncSession):
        all_objects = await session.execute(select(self.model))
        return all_objects.unique().scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
    ):
        obj_in_data = obj_in.model_dump(exclude_none=True)
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, update_data, db_obj, session: AsyncSession):
        obj_data = jsonable_encoder(db_obj)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj, session: AsyncSession):
        await session.delete(db_obj)
        await session.commit()
        return db_obj
