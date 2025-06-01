from pydantic import BaseModel, Field
from typing import Optional


class CreateUser(BaseModel):
    username: str
    password: str


class ReadUser(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes= True



class CreateTask(BaseModel):
    title: str
    description: Optional[str] = None


class ReadTask(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool

    class Config:
        from_attributes= True


class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None