#pylint: disable=unused-argument
import pytest
from pydantic import ValidationError
from src.dto.request.address_request import AddressRequest


def assert_field_error_msg(exc_info, field, expected_msg):
    errors = exc_info.value.errors()
    assert any(error['loc'] == (field,) and expected_msg in error['msg'] for error in errors)


def test_valid_address_request():
    req = AddressRequest(
        user_id=1,
        street="rua Ipiranga",
        number="456",
        complement=None,
        neighborhood="Centro",
        city="São Paulo",
        state="SP",
        zip_code="01001-000",
        is_default=True
    )
    assert req.user_id == 1
    assert req.street == "rua Ipiranga"
    assert req.number == "456"
    assert req.complement is None
    assert req.neighborhood == "Centro"
    assert req.city == "São Paulo"
    assert req.state == "SP"
    assert req.zip_code == "01001-000"
    assert req.is_default is True


@pytest.mark.parametrize(
    "field,value,expected_msg",
    [
        ("street", "ru", "String should have at least 3 characters"),
        ("street", "r" * 101, "String should have at most 100 characters"),
        ("street", "@!$@%$#*&", "Fields contains invalid characters."),
        ("neighborhood", "ce", "String should have at least 3 characters"),
        ("neighborhood", "n" * 51, "String should have at most 50 characters"),
        ("neighborhood", "!@#####", "Fields contains invalid characters."),
        ("city", "s@", "String should have at least 3 characters"),
        ("city", "c" * 51, "String should have at most 50 characters"),
        ("city", "s@a Paul(o", "Fields contains invalid characters."),
        ("complement", "c" * 51, "String should have at most 50 characters"),
        ("complement", "@@@@", "Fields contains invalid characters."),
        ("state", "s", "String should have at least 2 characters"),
        ("state", "s" * 3, "String should have at most 2 characters"),
        ("state", "X@", "state invalid."),
    ]
)
def test_text_fields_validations(valid_address_data, field, value, expected_msg):
    data = valid_address_data.copy()
    data[field] = value
    with pytest.raises(ValidationError) as exc_info:
        AddressRequest(**data)
    assert expected_msg in str(exc_info.value)



def test_validate_zip_code_error():
    with pytest.raises(ValidationError) as exc_info:
        AddressRequest(
            user_id=1,
            street="rua Ipiranga",
            number="456",
            complement=None,
            neighborhood="Centro",
            city="São Paulo",
            state="SP",
            zip_code="1234_12121",  # Invalid zip code (too short)
            is_default=True
        )
    assert "zip code invalid." in str(exc_info.value)



def test_is_default_field():
    # No informing is_default, should default to True
    req = AddressRequest(
        user_id=1,
        street="rua Ipiranga",
        number="456",
        complement=None,
        neighborhood="Centro",
        city="São Paulo",
        state="SP",
        zip_code="01001-000"
    )
    assert req.is_default is True

    # Informing is_default as False, should still be False
    req2 = AddressRequest(
        user_id=1,
        street="rua Ipiranga",
        number="456",
        complement=None,
        neighborhood="Centro",
        city="São Paulo",
        state="SP",
        zip_code="01001-000",
        is_default=False
    )
    assert req2.is_default is False
