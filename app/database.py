from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_async_engine(DATABASE_URL, echo=True) # создания движка для ORM 


AsyncSessionLocal = sessionmaker( # подключение к базе 
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db(): # функция  для открытия бд 
    async with AsyncSessionLocal() as session:
        yield session


Base = declarative_base() # базовый класс для создания моделей 