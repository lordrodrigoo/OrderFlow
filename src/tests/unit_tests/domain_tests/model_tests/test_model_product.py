from src.domain.models.product import Product



def test_create_product():
    product = Product.create_product(
        name="cake",
        description="A delicious cake",
        category_id=1,
        price=999.99,
        is_available=True,
        preparation_time=20
    )
    assert isinstance(product, Product)
    assert product.name == "cake"
    assert product.description == "A delicious cake"
    assert product.category_id == 1
    assert product.price == 999.99
    assert product.is_available is True
    assert product.preparation_time == 20


def test_full_description_property():
    product = Product.create_product(
        name="cake",
        description="A delicious cake",
        category_id=1,
        price=999.99,
        is_available=True,
        preparation_time=20
    )
    expected_description = "cake: $999.99 - A delicious cake"
    assert product.full_description == expected_description


def test_from_entity():
    class MockProductEntity:
        def __init__(self):
            self.id = 1
            self.name = "cake"
            self.description = "A delicious cake"
            self.category_id = 1
            self.price = 999.99
            self.is_available = True
            self.preparation_time = 20
            self.created_at = None
            self.updated_at = None

    entity = MockProductEntity()
    product = Product.from_entity(entity)
    assert product.id == 1
    assert product.name == "cake"
    assert product.description == "A delicious cake"
    assert product.category_id == 1
    assert product.price == 999.99
    assert product.is_available is True
    assert product.preparation_time == 20
    assert product.created_at is None
    assert product.updated_at is None
