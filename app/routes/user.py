from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from app.database import get_db
from app import models, schemas
from app.core import security



router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=schemas.ReadUser)
async def register_user(user_data: schemas.CreateUser, db: AsyncSession = Depends(get_db)):
    query = select(models.User).where(models.User.username == user_data.username)
    result = await db.execute(query)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    hashed_password = security.get_password_hash(user_data.password)

    add_user = models.User(
        username=user_data.username,
        hashed_password=hashed_password
    )
    db.add(add_user)
    await db.commit()
    await db.refresh(add_user)

    return add_user



@router.post("/login")
async def login_user(user_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    query = select(models.User).where(models.User.username == user_data.username)   
    result = await db.execute(query)
    existing_username = result.scalars().first()
    
    if not existing_username or not security.verify_password(user_data.password, existing_username.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    jwt_token = security.create_access_token(data={"sub": str(existing_username.username)})
    return {"access_token": jwt_token, "token_type": "bearer"}



@router.get("/me", response_model=schemas.ReadUser)
async def user(current_user: models.User = Depends(security.get_current_user)):
    return current_user