from src.domain.models.address import Address


def test_create_address():
    address = Address.create_address(
        user_id=1,
        street="Main St",
        number="123",
        neighborhood="Downtown",
        city="Anytown",
        state="State",
        zip_code="12345",
        is_default=True,
        complement="Apt 4"
    )
    assert address.full_address == "Main St, 123, Apt 4, Anytown, State, 12345"
    assert address.is_default is True


def test_full_address_property_without_complement():
    address = Address(
        user_id=1,
        street="Main St",
        number="123",
        neighborhood="Downtown",
        city="Anytown",
        state="State",
        zip_code="12345",
        is_default=True,
        complement=None
    )
    assert address.full_address == "Main St, 123, Anytown, State, 12345"


def test_full_address_property_with_complement():
    address = Address(
        user_id=1,
        street="Main St",
        number="123",
        neighborhood="Downtown",
        city="Anytown",
        state="State",
        zip_code="12345",
        is_default=True,
        complement="Apt 4"
    )
    assert address.full_address == "Main St, 123, Apt 4, Anytown, State, 12345"
