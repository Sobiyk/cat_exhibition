from fastapi import Depends, status
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.cat import breed_crud
from app.schemas.breed import BreedDB

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
