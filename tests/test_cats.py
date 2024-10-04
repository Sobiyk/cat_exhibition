from fastapi import status
from httpx import AsyncClient


async def test_create_cat(ac: AsyncClient):
    new_breed = await ac.post('/api/v1/breed/', json={"name": "A"})
    assert new_breed.status_code == status.HTTP_201_CREATED
    new_cat = await ac.post(
        '/api/v1/cats/',
        json={
            "name": "first",
            "description": "cute",
            "color": "blue",
            "age": 43,
            "breed": "A"
        }
    )
    assert new_cat.status_code == status.HTTP_201_CREATED
    assert new_cat.json()["name"] == "first"
    assert new_cat.json()["age"] == 43
    assert new_cat.json()["color"] == "blue"
    assert new_cat.json()["description"] == "cute"
    assert new_cat.json()["breed"]["name"] == "A"

    new_cat_wrong_breed = await ac.post(
        '/api/v1/cats/',
        json={
            "name": "first",
            "description": "cute",
            "color": "blue",
            "age": 43,
            "breed": "wrong"
        }
    )

    assert new_cat_wrong_breed.status_code == status.HTTP_404_NOT_FOUND
    assert new_cat_wrong_breed.json() == {
        'detail': 'Породы с названием wrong не найдено.'
    }


async def test_list_cats(ac: AsyncClient):
    response = await ac.get('/api/v1/cats/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "name": "first",
        "description": "cute",
        "color": "blue",
        "age": 43,
        "id": 1,
        "breed": {"name": "A"}
    }]


async def test_get_cat_info(ac: AsyncClient):
    response = await ac.get('/api/v1/cats/1')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "name": "first",
        "description": "cute",
        "color": "blue",
        "age": 43,
        "id": 1,
        "breed": {"name": "A"}
    }

    response = await ac.get('/api/v1/cats/12')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Объекта с id 12 не найдено.'}


async def test_update_cat(ac: AsyncClient):
    response = await ac.patch(
        '/api/v1/cats/1',
        json={
            "name": "updated",
            "description": "fast",
            "color": "black",
            "age": 44,
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
            "name": "updated",
            "description": "fast",
            "color": "black",
            "id": 1,
            "breed": {"name": "A"},
            "age": 44,
        }

    response = await ac.patch(
        '/api/v1/cats/111',
        json={"name": "updated"}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Объекта с id 111 не найдено.'}

    response = await ac.patch(
        '/api/v1/cats/1',
        json={
            "breed": "Blah Blah"
        }
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Породы с названием Blah Blah не найдено.'}


async def test_remove_cat(ac: AsyncClient):
    response = await ac.delete('/api/v1/cats/1')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b''

    response = await ac.delete('/api/v1/cats/12')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Объекта с id 12 не найдено.'}
