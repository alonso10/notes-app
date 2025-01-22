from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.future import select

from asyncpg.exceptions import (
    IdleSessionTimeoutError as LockWaitTimeout,
    DeadlockDetectedError,
)

from app.database.models.notes_model import NoteModel
from app.schemas.notes.schema import CreateNoteSchema, NoteBaseSchema
from app.services.errors import NoteNotFoundException, NoteUpdateBlockedException


class NoteService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, note: CreateNoteSchema):
        model = NoteModel(**note.model_dump())
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def get_all(self, user_id: int):
        return (
            (await self.db.execute(select(NoteModel).filter_by(user_id=user_id)))
            .scalars()
            .all()
        )

    async def get_by_id(self, note_id: int, user_id: int):
        result = await self.db.execute(
            text("SELECT * FROM notes WHERE id=:note_id AND user_id=:user_id"),
            {"note_id": note_id, "user_id": user_id},
        )
        row = result.fetchone()
        if not row:
            raise NoteNotFoundException()

        db_note = await self.db.get(NoteModel, row.id)
        return db_note

    async def update(self, note_id: int, note: NoteBaseSchema, user_id: int):
        try:
            result = await self.db.execute(
                text("""
                       SELECT * 
                       FROM notes 
                       WHERE id = :note_id AND user_id = :user_id 
                       FOR UPDATE
                   """),
                {"note_id": note_id, "user_id": user_id},
            )
            row = result.fetchone()
            if not row:
                raise NoteNotFoundException()

            db_note = await self.db.get(NoteModel, note_id)
            db_note.title = note.title
            db_note.content = note.content
            await self.db.commit()
            await self.db.refresh(db_note)
            return db_note
        except (LockWaitTimeout, DeadlockDetectedError):
            raise NoteUpdateBlockedException()

    async def delete(self, note_id: int, user_id: int):
        result = await self.db.execute(
            text("""
                SELECT * FROM notes 
                WHERE id=:note_id AND user_id=:user_id 
            """),
            {"note_id": note_id, "user_id": user_id},
        )
        row = result.fetchone()
        if not row:
            raise NoteNotFoundException()

        db_note = await self.db.get(NoteModel, note_id)
        await self.db.delete(db_note)
        await self.db.commit()
        return {"msg": "Note deleted"}
