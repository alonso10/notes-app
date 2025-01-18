from sqlalchemy.orm import Session
from sqlalchemy import text

from psycopg2.errors import DeadlockDetected, IdleSessionTimeout as LockWaitTimeout

from app.database.models.notes_model import NoteModel
from app.schemas.notes.schema import CreateNoteSchema, NoteBaseSchema
from app.services.errors import NoteNotFoundException, NoteUpdateBlockedException


class NoteService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, note: CreateNoteSchema):
        model = NoteModel(**note.model_dump())
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_all(self, user_id: int):
        return self.db.query(NoteModel).filter(NoteModel.user_id == user_id).all()

    def get_by_id(self, note_id: int, user_id: int):
        note = (
            self.db.query(NoteModel)
            .filter(NoteModel.id == note_id, NoteModel.user_id == user_id)
            .first()
        )
        if not note:
            raise NoteNotFoundException()
        return note

    def update(self, note_id: int, note: NoteBaseSchema, user_id: int):
        try:
            result = self.db.execute(
                text(
                    "SELECT * FROM notes WHERE id = :note_id AND user_id = :user_id FOR UPDATE"
                ),
                {"note_id": note_id, "user_id": user_id},
            )
            row = result.fetchone()
            if not row:
                raise NoteNotFoundException()

            note_found = (
                self.db.query(NoteModel)
                .filter(NoteModel.id == note_id, NoteModel.user_id == user_id)
                .first()
            )
            note_found.title = note.title
            note_found.content = note.content
            self.db.commit()
            self.db.refresh(note_found)
            return note_found
        except (LockWaitTimeout, DeadlockDetected):
            raise NoteUpdateBlockedException()


    def delete(self, note_id: int, user_id: int):
        note_found = (
            self.db.query(NoteModel)
            .filter(NoteModel.id == note_id, NoteModel.user_id == user_id)
            .first()
        )
        if not note_found:
            raise NoteNotFoundException()

        self.db.delete(note_found)
        self.db.commit()
        return {"msg": "Note deleted"}
