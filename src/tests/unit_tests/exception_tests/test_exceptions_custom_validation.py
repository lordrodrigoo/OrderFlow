from unittest.mock import MagicMock
import json
import pytest
from fastapi.exceptions import RequestValidationError
from fastapi import status
from src.exceptions.custom_validation_exceptions import pydantic_validation_handler


@pytest.mark.asyncio
async def test_pydantic_validation_handler():
    request = MagicMock()
    exc = MagicMock(spec=RequestValidationError)
    exc.errors.return_value = [{"msg": "Value error, invalid field"}]
    response = await pydantic_validation_handler(request, exc)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.asyncio
async def test_pydantic_validation_handler_strips_prefix():
    request = MagicMock()
    exc = MagicMock(spec=RequestValidationError)
    exc.errors.return_value = [{"msg": "Value error, invalid field"}]
    response = await pydantic_validation_handler(request, exc)

    body = json.loads(response.body)
    assert body["message"] == "invalid field"
