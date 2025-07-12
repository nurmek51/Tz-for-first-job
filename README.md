# TZ for first job Backend

## Описание
Простое серверное приложение для учёта продаж на FastAPI с использованием PostgreSQL.

## Быстрый старт

1. **Создайте и настройте .env:**
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/firstjob_db
   ```
   Замените `user`, `password`, `localhost`, `5432`, `firstjob_db` на свои значения.

2. **Установите зависимости:**
   ```bash
   pip install fastapi[all] sqlalchemy[asyncio] python-dotenv
   ```

3. **Запустите сервер:**
   ```bash
   uvicorn main:app --reload
   ```

4. **Документация API:**
   - Swagger: http://localhost:8000/docs

## Структура проекта
- `main.py` — точка входа FastAPI
- `models.py` — SQLAlchemy модели
- `schemas.py` — Pydantic схемы
- `database.py` — подключение к БД
- `routers/` — роутеры для продуктов и продаж

## Примечания
- Таблицы создаются автоматически при первом запуске.
- Для работы требуется PostgreSQL. 