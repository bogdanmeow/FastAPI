from fastapi import FastAPI, Cookie, Form, Query
from typing import Annotated
from pydantic import BaseModel
import uuid
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

# Help list
#=========================
# uvicorn main:app --reload # Команда запуска сервера
#=========================
# pip install 'fastapi-users[sqlalchemy]'
# pip install SQLAlchemy # Библиотека для работы с БД
# pip install python-multipart # Для использования Form # для получений Form Data вместо JSON
#=========================
# POST — создает данные
# GET — читает данные
# PUT — обновляет данные
# DELETE — удаляет данные
#=========================
#действие return: Можно вернуть dict, list или одиночные значения: str, int и так далее. Также модели Pydantic.
#=========================

app = FastAPI()

@app.get("/")
async def root():
    return {'Бронирование Отелей'}

@app.post('/login/')
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {'username': username}

@app.post('/register')
async def register(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {'username': username}

@app.get("/Cookie")
async def cookie(cookie_id: Annotated[str | None, Cookie()] = None):
    return {'cookie_id': cookie_id}

#========================================

@app.post('/users/add')
async def add_user(username: Annotated[str, Query(min_length=4)]): # async def add_user(username: Annotated[str]): #не работает такой вариант (по примеру с занятия)
    user_id: uuid.uuid4()
    user = User(id = user_id, username=username)
    users.append(user)
    return f'User id: {user_id}'

#========================================

