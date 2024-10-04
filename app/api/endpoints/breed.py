from fastapi import Depends, status
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.cat import breed_crud
from app.schemas.breed import BreedDB, CatBreedDB

router = APIRouter(
    prefix='/breed',
    tags=['Породы']
)


@router.get(
    '/',
    response_model=list[BreedDB],
    status_code=status.HTTP_200_OK
)
async def list_breeds(session: AsyncSession = Depends(get_async_session)):
    """
    Вывести список всех пород.

    Возвращает:
        Словарь, содержащий список всех пород с информацией о них
        (id, name).
    """
    return await breed_crud.get_multi(session)


@router.post(
    '/',
    response_model=BreedDB,
    status_code=status.HTTP_201_CREATED
)
async def create_breed(
    breed_in: CatBreedDB,
    session: AsyncSession = Depends(get_async_session)
):
    breed = await breed_crud.create(breed_in, session)
    return breed
