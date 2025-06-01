from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from fastapi import Query
from app.database import get_db
from app import models, schemas
from app.core.security import get_current_user  
from django.db import router


router = APIRouter(prefix="/task", tags=["tasks"])



@router.post("/create", response_model=schemas.ReadTask)
async def create_task(task_data: schemas.CreateTask, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_task = models.Task(
        title = task_data.title,
        description = task_data.description,
        owner_id = current_user.id,
        completed = False
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return new_task



@router.get("/all", response_model=List[schemas.ReadTask])
async def get_all_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    page: int = Query(1, ge=1)  # номер страницы, по умолчанию первая
):
    limit = 5  # фиксируем лимит
    offset = (page - 1) * limit

    query = (
        select(models.Task)
        .where(models.Task.owner_id == current_user.id)
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(query)
    tasks = result.scalars().all()

    return tasks


@router.put("/{task_id}/complete", response_model=schemas.ReadTask)
async def complete_task(task_data: schemas.UpdateTask, task_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    query = select(models.Task).where(models.Task.id == task_id, models.Task.owner_id == current_user.id)
    result = await db.execute(query)
    task = result.scalars().first()

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.completed is not None:
        task.completed = task_data.completed


    await db.commit()
    await db.refresh(task)

    return task


@router.delete("/{task_id}/delete", response_model=schemas.ReadTask)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    query = select(models.Task).where(models.Task.id == task_id, models.Task.owner_id == current_user.id)
    result = await db.execute(query)
    task = result.scalars().first()

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    await db.delete(task)
    await db.commit()
   


    return task


@router.get("/search", response_model=List[schemas.ReadTask])
async def search_tasks(
    title: Optional[str] = Query(None, description="Поисковый запрос по заголовку задачи"),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = select(models.Task).where(models.Task.owner_id == current_user.id)

    if title:
        query = query.where(models.Task.title.ilike(f"%{title}%"))

    result = await db.execute(query)
    tasks = result.scalars().all()

    return tasks
