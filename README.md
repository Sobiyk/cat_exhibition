# Cats exhibition admin


### Шаблон заполнения .env:

```
APP_NAME='string'
APP_VERSION='1.0.0'
DATABASE_URL='postgresql+asyncpg://postgres:postgres@localhost:1234/db'
```

### Запустить сборку контейнеров
```
docker-compose up -d --build
```

### Перейти в документацию
```
http://localhost:8000/docs
```

### Запустить тесты
```
pytest
```
