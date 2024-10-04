# cities_info


### Шаблон заполнения .env:

```
APP_NAME='string'
APP_VERSION='1.0.0'
DATABASE_URL='postgresql+asyncpg://postgres:postgres@localhost:1234/db_name'
```

### Запустить сборку контейнеров
```
docker-compose up -d --build
```

### Применить миграции
```
docker exec -it pets_test_assigment-web-1 bash
alembic upgrade head
```

### Перейти в документацию
```
http://localhost:8000/docs
```