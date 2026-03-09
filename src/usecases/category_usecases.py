from src.domain.models.category import Category
from src.dto.request.category_request import CategoryRequest
from src.dto.response.category_response import CategoryResponse
from src.domain.repositories.category_repository import CategoryRepositoryInterface
from src.exceptions.exception_handlers_category import (
    CategoryNotFoundException,
    CategoryAlreadyExistsException
)



class CategoryUsecase:
    def __init__(self, category_repository: CategoryRepositoryInterface):
        self.category_repository = category_repository

    def create_category(self, category_request: CategoryRequest) -> CategoryResponse:
        if self.category_repository.find_category_by_name(category_request.name):
            raise CategoryAlreadyExistsException(category_name=category_request.name)

        category_entity = Category (
            name=category_request.name,
            description=category_request.description,
        )
        created_category = self.category_repository.create_category(category_entity)
        return CategoryResponse(**created_category.__dict__)


    def update_category(
            self,
            category_id: int,
            category_request: CategoryRequest
        ) -> CategoryResponse:

        if not self.category_repository.get_category_by_id(category_id):
            raise CategoryNotFoundException(category_id)

        existing = self.category_repository.get_category_by_id(category_id)
        if existing and existing.id != category_id and existing.name == category_request.name:
            raise CategoryAlreadyExistsException(category_name=category_request.name)


        category_entity = Category (
            id=category_id,
            name=category_request.name,
            description=category_request.description,
        )

        updated_category = self.category_repository.update_category(category_entity)
        return CategoryResponse(**updated_category.__dict__)


    def get_category_by_id(self, category_id: int) -> CategoryResponse:
        category = self.category_repository.get_category_by_id(category_id)
        if not category:
            raise CategoryNotFoundException(category_id)
        return CategoryResponse(**category.__dict__)



    def list_categories(self) -> list[CategoryResponse]:
        categories = self.category_repository.get_all_categories()
        return [CategoryResponse(**category.__dict__) for category in categories]


    def delete_category(self, category_id: int) -> bool:
        if not self.category_repository.get_category_by_id(category_id):
            raise CategoryNotFoundException(category_id)
        return self.category_repository.delete_category(category_id)
