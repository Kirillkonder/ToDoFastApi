import os
from datetime import datetime, timedelta
from typing import Union
from sqlalchemy import select
from passlib.context import CryptContext
from jose import jwt
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from rest_framework import status
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app import models
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return crypto_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypto_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy() # сюда копируються данные пользоватля
    if expires_delta:
        expire = datetime.utcnow() + expires_delta # время жизни токена
    else:
        expire = datetime.utcnow() + timedelta(minutes=15) # время жизни токена 

    to_encode.update({"exp": expire}) # добавляю время жизни токена в словарь 
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # создаю токен

    return encoded_jwt # возвращаю токен


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
    stmt = select(models.User).where(models.User.username == username)
    result = await db.execute(stmt)
    existing_user = result.scalars().first()

    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return existing_user