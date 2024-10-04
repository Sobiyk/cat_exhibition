from typing_extensions import Annotated, Optional

from fastapi import Depends, Path, Query, status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.cat import cat_crud
from app.exceptions.crud.base import ObjectIDNotFoundException
from app.exceptions.crud.breed import BreedNotFoundException
from app.schemas.cat import CatCreate, CatDB, CatUpdate

router = APIRouter(
    prefix='/cats',
    tags=['Котики']
)


@router.get(
    '/',
    response_model=list[CatDB],
    status_code=status.HTTP_200_OK
)
async def list_cats(
    breed: Annotated[Optional[list[str]], Query(max_length=50)] = None,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получить список всех котиков.

    Аргументы:
        breed (list[str]): Для вывода котиков только соответствущих пород.

    Возвращает:
        Словарь, содержащий список всех котиков с информацией о них
        (id, name, breed, color, age, description).
    """
    return await cat_crud.get_multi_filter_by_breed(breed, session)


@router.get(
    '/{cat_id}',
    response_model=CatDB,
    status_code=status.HTTP_200_OK
)
async def get_cat_info(
    cat_id: Annotated[int, Path(gt=0)],
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получить информацию о котике по id.

    Аргументы:
        cat_id (int): ID котика, информацию о котором мы хотим получить.

    Возвращает:
        Словарь, содержащий информацию о котике
        (id, name, breed, color, age, description).

    Исключения:
        HTTPException (404): Если котик с указанным id не найден.
        HTTPException (422): Если указан некорректный id котика.
    """
    try:
        cat = await cat_crud.get(cat_id, session)
    except ObjectIDNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return cat


@router.post(
    '/',
    response_model=CatDB,
    status_code=status.HTTP_201_CREATED
)
async def create_cat(
    cat_in: CatCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Добавить котика в базу.

    Аргументы:
        cat_in (CatCreate): Словарь с данными о котике,
        которого мы хотим создать.

    Возвращает:
        Словарь, содержащий информацию о созданном котике котике
        (id, name, breed, color, age, description).

    Исключения:
        HTTPException (404): Если породы с указанным названием не найдено.
        HTTPException (422): Если данные котика не прошли валидацию.
    """
    try:
        cat = await cat_crud.create(cat_in, session)
    except BreedNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return cat


@router.patch(
    '/{cat_id}',
    response_model=CatDB
)
async def update_cat(
    cat_id: Annotated[int, Path(gt=0)],
    update_data: CatUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Изменить информацию о котике по id.

    Аргументы:
        cat_in (CatCreate): Словарь с данными котика,
        которые мы хотим изменить.

    Возвращает:
        Словарь, содержащий обновленную информацию о котике
        (id, name, breed, color, age, description).

    Исключения:
        HTTPException (404): Если котик с указанным id не найден.
        HTTPException (404): Если породы с указанным именем не найдено.
        HTTPException (422): Если указан некорректный id котика.
        HTTPException (422): Если данные для обновления не прошли валидацию.
    """
    try:
        cat = await cat_crud.get(cat_id, session)
    except ObjectIDNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    try:
        cat_updated = await cat_crud.update(update_data, cat, session)
    except BreedNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return cat_updated


@router.delete(
    '/{cat_id}'
)
async def remove_cat(
    cat_id: Annotated[int, Path(gt=0)],
    session: AsyncSession = Depends(get_async_session)
):
    """
    Удалить котика.

    Аргументы:
        cat_id (int): ID котика, информацию о котором мы хотим получить.

    Возвращает:
        Пустой ответ.

    Исключения:
        HTTPException (404): Если котик с указанным id не найден.
        HTTPException (422): Если указан некорректный id котика.
    """
    try:
        cat = await cat_crud.get(cat_id, session)
    except ObjectIDNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    await cat_crud.remove(cat, session)
    return
