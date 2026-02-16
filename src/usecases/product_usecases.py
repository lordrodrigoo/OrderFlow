from fastapi import HTTPException
from src.domain.models.product import Product
from src.dto.request.product_request import ProductRequest
from src.dto.response.product_response import ProductResponse
from src.domain.repositories.product_repository import ProductRepositoryInterface


class ProductUsecase:
    def __init__(self, product_repository: ProductRepositoryInterface):
        self.product_repository = product_repository


    def create_product(self, product_request: ProductRequest) -> ProductResponse:
        if not self.product_repository.find_products_by_category(
            product_request.category_id
        ):
            raise HTTPException(status_code=404, detail="Category not found")

        data = product_request.model_dump()
        product_entity = Product(**data)

        created_product = self.product_repository.create_product(product_entity)
        return ProductResponse(**created_product.__dict__)

    def update_product(
            self,
            product_id: int,
            product_request: ProductRequest
        ) -> ProductResponse:

        if not self.product_repository.find_product_by_id(product_id):
            raise HTTPException(status_code=404, detail="Product not found")

        data = product_request.model_dump()
        data["id"] = product_id
        product_entity = Product(**data)

        updated_product = self.product_repository.update_product(product_entity)
        return ProductResponse(**updated_product.__dict__)
