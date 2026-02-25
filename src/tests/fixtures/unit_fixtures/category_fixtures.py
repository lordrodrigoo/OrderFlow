from datetime import datetime
from unittest.mock import MagicMock
import pytest


@pytest.fixture
def category_repository_mock():
    repository_mock = MagicMock()
    repository_mock.find_by_name.return_value = None
    repository_mock.create_category.return_value = MagicMock(
        id=1,
        name="Pizzas",
        description="Categoria de pizzas deliciosas",
        created_at=datetime.now()
    )
    return repository_mock
