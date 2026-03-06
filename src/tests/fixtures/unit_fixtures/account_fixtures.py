#pylint: disable=redefined-outer-name
from unittest.mock import MagicMock
import pytest



@pytest.fixture
def account_repository_mock():
    return MagicMock()
