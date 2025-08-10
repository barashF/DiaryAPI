from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EntryBase(BaseModel):
    title: str
    content: str


class EntryCreate(EntryBase):
    pass


class EntryUpdate(EntryBase):
    title: Optional[str] = None
    content: Optional[str] = None
    is_done: Optional[bool] = None


class Entry(EntryBase):
    id: int
    is_done: bool
    created_at: datetime

    
    class Config:
        orm_mode = True