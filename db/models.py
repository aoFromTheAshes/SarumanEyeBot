from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"  

    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_id: int = Field(index=True, unique=True, nullable=False)
    username: Optional[str] = Field(nullable=True, max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    tasks: list["Task"] = Relationship(back_populates="user")


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")  
    name: str = Field(nullable=False)
    duration: Optional[int] = Field(nullable=True)  
    start_time: int = Field(nullable=True)
    end_time: int = Field(nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: User = Relationship(back_populates="tasks")