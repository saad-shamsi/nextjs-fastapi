from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: Optional[datetime] = Field(default=None)


class Todo(BaseModel, table=True):
    title: str = Field(nullable=False, index=True, max_length=100)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)


class TodoCreate(SQLModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False


class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
