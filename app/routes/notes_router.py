from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config.bootstrap import init_auth_user_service, init_notes_service
from app.database.models.user_model import UserModel
from app.schemas.notes.schema import NoteBaseSchema, CreateNoteSchema
from app.services.notes.service import NoteService
from app.services.user.auth_service import UserAuthService

notes_router = APIRouter(prefix="/notes", tags=["notes"])
security = HTTPBearer()


def auth_required(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserAuthService = Depends(init_auth_user_service),
):
    return user_service.authenticate(credentials.credentials)


@notes_router.post("")
def create_note(
    request: NoteBaseSchema,
    user: UserModel = Depends(auth_required),
    note_service: NoteService = Depends(init_notes_service),
):
    return note_service.create(
        CreateNoteSchema(user_id=user.id, title=request.title, content=request.content)
    )


@notes_router.get("")
def get_all_notes(
    user: UserModel = Depends(auth_required),
    note_service: NoteService = Depends(init_notes_service),
):
    return note_service.get_all(user.id)


@notes_router.get("/{note_id}")
def get_note_by_id(
    note_id: int,
    user: UserModel = Depends(auth_required),
    note_service: NoteService = Depends(init_notes_service),
):
    return note_service.get_by_id(note_id, user.id)


@notes_router.put("/{note_id}")
def update_note_by_id(
    note_id: int,
    request: NoteBaseSchema,
    user: UserModel = Depends(auth_required),
    note_service: NoteService = Depends(init_notes_service),
):
    return note_service.update(note_id, request, user.id)


@notes_router.delete("/{note_id}")
def delete_note_by_id(
    note_id: int,
    user: UserModel = Depends(auth_required),
    note_service: NoteService = Depends(init_notes_service),
):
    return note_service.delete(note_id, user.id)
