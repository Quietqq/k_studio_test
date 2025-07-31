# Audio Conversion Service

Сервис для конвертации аудиозаписей из WAV в MP3 с хранением в PostgreSQL

## Требования
- Docker 20+
- Docker Compose 2.0+
- Python 3.12 (для локальной разработки)

## Быстрый старт

```bash
git clone https://github.com/Quietqq/k_studio_test.git
cd k_studio_test

# создайте свой .env файл со следующими значениями

POSTGRES_USER=ваш_пользователь
POSTGRES_PASSWORD=ваш_пароль
POSTGRES_DB=имя_базы

JWT_SECRET=ваш_секретный_ключ

docker compose up -d --build

Сервис будет доступен на `http://localhost:8000`


Документация API будет доступна на: http://localhost:8000/docs

## Полная документация API

### 1. Создание пользователя
```bash
POST /users/
Content-Type: application/json

{
  "name": "username"
}
```

Пример ответа:
```json
{
  "id": "uuid пользователя",
  "token": "токен для доступа"
}
```

### 2. Загрузка аудио
```bash
POST /upload?user_id={user_id}
Content-Type: multipart/form-data
Token: {ваш_токен}

file: ваш_файл.wav
```

Пример ответа:
```json
{
  "download_url": "http://localhost:8000/record?id=file_id&user=user_id"
}
```

### 3. Скачивание аудио
Просто откройте в браузере ссылку из предыдущего шага или:
```bash
GET /record?id={file_id}&user={user_id}
```


## Технологии
- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- FFmpeg
- Docker