from src.domain.models.product import Product
from src.dto.request.product_request import ProductRequest
from src.dto.response.product_response import ProductResponse
from src.domain.repositories.product_repository import ProductRepositoryInterface
from src.exceptions.exception_handlers_product import (
    ProductNotFoundException,
    ProductAlreadyExistsException,
    ProductCategoryNotFoundException,
    InvalidPriceProductException
)
from src.infra.db.repositories.category_repository_interface import CategoryRepositoryInterface



class ProductUsecase:
    def __init__(self, product_repository: ProductRepositoryInterface, category_repository: CategoryRepositoryInterface):
        self.product_repository = product_repository
        self.category_repository = category_repository



    def create_product(self, product_request: ProductRequest) -> ProductResponse:
        if self.product_repository.find_products_by_name(product_request.name):
            raise ProductAlreadyExistsException(product_name=product_request.name)

        if not self.category_repository.get_category_by_id(product_request.category_id):
            raise ProductCategoryNotFoundException(category_id=product_request.category_id)


        if product_request.price <= 0:
            raise InvalidPriceProductException()

        product_entity = Product (
            name=product_request.name,
            description=product_request.description,
            category_id=product_request.category_id,
            price=product_request.price,
            is_available=product_request.is_available,
            preparation_time=product_request.preparation_time,
        )

        created_product = self.product_repository.create_product(product_entity)
        return ProductResponse(**created_product.__dict__)

    def update_product(
            self,
            product_id: int,
            product_request: ProductRequest
        ) -> ProductResponse:

        if not self.product_repository.find_product_by_id(product_id):
            raise ProductNotFoundException(product_id)

        existing = self.product_repository.find_product_by_id(product_id)
        if existing and existing.id != product_id and existing.name == product_request.name:
            raise ProductAlreadyExistsException(product_name=product_request.name)

        product_entity = Product (
            id=product_id,
            name=product_request.name,
            description=product_request.description,
            price=product_request.price,
            category_id=product_request.category_id,
            is_available=product_request.is_available,
            preparation_time=product_request.preparation_time
        )

        updated_product = self.product_repository.update_product(product_entity)
        return ProductResponse(**updated_product.__dict__)


    def get_product_by_id(self, product_id: int) -> ProductResponse:
        product = self.product_repository.find_product_by_id(product_id)
        if not product:
            raise ProductNotFoundException(product_id=product_id)
        return ProductResponse(**product.__dict__)


    def find_products_by_category(self, category_id: int) -> list[ProductResponse]:
        if not self.category_repository.get_category_by_id(category_id):
            raise ProductCategoryNotFoundException(category_id=category_id)

        products = self.product_repository.find_products_by_category(category_id)
        return [ProductResponse(**product.__dict__) for product in products]


    def count_products_by_category(self, category_id: int) -> int:
        if not self.category_repository.get_category_by_id(category_id):
            raise ProductCategoryNotFoundException(category_id=category_id)

        return self.product_repository.count_products_by_category(category_id)


    def list_products(
        self,
        name: str = None,
        category_id: int = None,
        is_available: bool = None,
        min_price: float = None,
        max_price: float = None,
        skip: int = 0,
        limit: int = 10
    ) -> list[ProductResponse]:
        products = []

        if name:
            products = self.product_repository.find_products_by_name(name)
        elif category_id:
            products = self.product_repository.find_products_by_category(category_id)
        elif is_available is not None:
            products = self.product_repository.find_products_by_availability(is_available)
        elif min_price is not None and max_price is not None:
            products = self.product_repository.find_products_by_price_range(min_price, max_price)
        else:
            products = self.product_repository.get_all_products()

        # Pagination
        products = products[skip: skip + limit] if products else []
        return [ProductResponse(**product.__dict__) for product in products]



    def delete_product(self, product_id: int) -> bool:
        if not self.product_repository.find_product_by_id(product_id):
            raise ProductNotFoundException(product_id=product_id)
        return self.product_repository.delete_product(product_id)
