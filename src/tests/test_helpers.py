from unittest.mock import MagicMock
import pytest
from pydantic import BaseModel, Field
from src.tests.helpers import FakeDBConnectionHandler, get_error_msg, _call_handler


def test_fake_db_connection_handler_get_session():
    session_mock = MagicMock()
    handler = FakeDBConnectionHandler(session_mock)
    assert handler.get_session() is session_mock


def test_get_error_msg_returns_none_when_field_not_found():
    class DummyModel(BaseModel):
        value: int = Field(..., gt=0)

    with pytest.raises(Exception) as exc_info:
        DummyModel(value=-1)

    result = get_error_msg(exc_info, "nonexistent_field")
    assert result is None


@pytest.mark.asyncio
async def test_call_handler():
    received = {}

    async def fake_handler(request, exc):
        received["request"] = request
        return f"handled:{exc}"

    result = await _call_handler(fake_handler, "test_error")
    assert result == "handled:test_error"
    assert isinstance(received["request"], MagicMock)
