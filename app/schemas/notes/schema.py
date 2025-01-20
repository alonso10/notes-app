from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NoteBaseSchema(BaseModel):
    title: str
    content: Optional[str] = None


class CreateNoteSchema(NoteBaseSchema):
    user_id: int


class NoteSchema(NoteBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True
