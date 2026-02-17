#pylint: disable=unused-argument
import pytest
from pydantic import ValidationError
from src.dto.request.address_request import AddressRequest
from src.tests import helpers



def test_valid_address_request(valid_address_data):
    req = AddressRequest(**valid_address_data)
    assert req.user_id == 1
    assert req.street == "Rua Exemplo"
    assert req.zip_code == "12345-678"


@pytest.mark.parametrize(
    "field,value,expected_msg",
    [
        ("street", "ru", "String should have at least 3 characters"),
        ("street", "r" * 101, "String should have at most 100 characters"),
        ("street", "@!$@%$#*&", "street must contain letters or numbers"),
        ("neighborhood", "ce", "String should have at least 3 characters"),
        ("neighborhood", "!@#####", "neighborhood must contain only letters."),
        ("city", "s@a Paul(o", "city must contain only letters."),
        ("complement", "@@@@", "complement must contain letters, numbers, or hyphens."),
        ("state", "X@", "invalid Brazilian state (UF)."),
    ]
)
def test_text_fields_validations(valid_address_data, field, value, expected_msg):
    data = valid_address_data.copy()
    data[field] = value

    with pytest.raises((ValidationError, ValueError)) as exc_info:
        AddressRequest(**data)
    assert expected_msg in helpers.get_error_msg(exc_info, field)



def test_validate_zip_normalized(valid_address_data):
    data = valid_address_data.copy()
    data["zip_code"] = "1234_12121"
    with pytest.raises(ValidationError) as exc_info:
        AddressRequest(**data)
    assert "zip code must have exactly 8 digits." in helpers.get_error_msg(exc_info, "zip_code")




def test_is_default_field(valid_address_data):
    req = AddressRequest(**valid_address_data)
    assert req.is_default is True

    data = valid_address_data.copy()
    data["is_default"] = False
    req2 = AddressRequest(**data)
    assert req2.is_default is False
