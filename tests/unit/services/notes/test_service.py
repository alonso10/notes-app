from unittest import IsolatedAsyncioTestCase
from unittest.mock import create_autospec, call

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import NoteModel
from app.schemas.notes.schema import CreateNoteSchema
from app.services.notes.service import NoteService


@pytest.mark.unit
class TestService(IsolatedAsyncioTestCase):
    @pytest.mark.asyncio
    async def test_create_note(self) -> None:
        mock_session = create_autospec(AsyncSession, instance=True)

        service = NoteService(mock_session)
        new_note = CreateNoteSchema(
            title="Test Note", content="This is a test note", user_id=1
        )

        expected_output = NoteModel(**new_note.model_dump())
        output = await service.create(new_note)

        expected_session_calls = [
            call.add(output),
            call.commit(),
            call.refresh(output),
        ]

        self.assertEqual(output.title, expected_output.title)
        self.assertEqual(output.content, expected_output.content)
        self.assertIn(expected_session_calls, mock_session.mock_calls)
