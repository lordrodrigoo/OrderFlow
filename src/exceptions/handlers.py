from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from src.exceptions.custom_validation_exceptions import pydantic_validation_handler

from src.exceptions.exception_handlers_user import (
    EmailAlreadyExistsException, email_exception_handler,
    UserNotFoundException, user_not_found_exception_handler,
    UserPermissionDeniedException, user_permission_denied_exception_handler,
)
from src.exceptions.exception_handlers_address import (
    AddressAlreadyExistsException, address_already_exists_exception_handler,
    AddressNotFoundException, address_not_found_exception_handler,
    AddressPermissionDeniedException, address_permission_denied_exception_handler,
)
from src.exceptions.exception_handlers_product import (
    ProductNotFoundException, product_not_found_exception_handler,
    ProductAlreadyExistsException, product_already_exists_exception_handler,
    ProductCategoryNotFoundException, product_category_not_found_exception_handler,
    InvalidPriceProductException, invalid_price_product_exception_handler,
)
from src.exceptions.exception_handlers_category import (
    CategoryNotFoundException, category_not_found_exception_handler,
    CategoryAlreadyExistsException, category_already_exists_exception_handler,
)
from src.exceptions.exception_handlers_order import (
    OrderNotFoundException, order_not_found_exception_handler,
    OrderAlreadyCanceledException, order_already_canceled_exception_handler,
)
from src.exceptions.exception_handlers_order_item import (
    OrderItemNotFoundException, order_item_not_found_exception_handler,
    InvalidOrderItemException, invalid_order_item_exception_handler,
    DuplicateOrderItemException, duplicate_order_item_exception_handler,
)
from src.exceptions.exception_handlers_review import (
    ReviewNotFoundException, review_not_found_exception_handler,
    InvalidReviewException, invalid_review_exception_handler,
)
from src.exceptions.exception_handlers_auth import (
    TokenExpiredException, token_expired_exception_handler,
    TokenInvalidException, token_invalid_exception_handler,
    InvalidCredentialsException as AuthInvalidCredentialsException,
    invalid_credentials_exception_handler as auth_invalid_credentials_exception_handler,
)
from src.exceptions.exception_handlers_account import (
    InvalidCredentialsException, invalid_credentials_exception_handler,
    AccountInactiveException, account_inactive_exception_handler,
    AccountNotFoundException, account_not_found_exception_handler,
    AccountPermissionDeniedException, account_permission_denied_exception_handler,
    UsernameAlreadyExistsException, username_exception_handler
)


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(RequestValidationError, pydantic_validation_handler)
    app.add_exception_handler(EmailAlreadyExistsException, email_exception_handler)
    app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
    app.add_exception_handler(UserPermissionDeniedException, user_permission_denied_exception_handler)
    app.add_exception_handler(AddressAlreadyExistsException, address_already_exists_exception_handler)
    app.add_exception_handler(AddressNotFoundException, address_not_found_exception_handler)
    app.add_exception_handler(AddressPermissionDeniedException, address_permission_denied_exception_handler)
    app.add_exception_handler(ProductNotFoundException, product_not_found_exception_handler)
    app.add_exception_handler(ProductAlreadyExistsException, product_already_exists_exception_handler)
    app.add_exception_handler(ProductCategoryNotFoundException, product_category_not_found_exception_handler)
    app.add_exception_handler(InvalidPriceProductException, invalid_price_product_exception_handler)
    app.add_exception_handler(CategoryNotFoundException, category_not_found_exception_handler)
    app.add_exception_handler(CategoryAlreadyExistsException, category_already_exists_exception_handler)
    app.add_exception_handler(OrderNotFoundException, order_not_found_exception_handler)
    app.add_exception_handler(OrderAlreadyCanceledException, order_already_canceled_exception_handler)
    app.add_exception_handler(OrderItemNotFoundException, order_item_not_found_exception_handler)
    app.add_exception_handler(InvalidOrderItemException, invalid_order_item_exception_handler)
    app.add_exception_handler(DuplicateOrderItemException, duplicate_order_item_exception_handler)
    app.add_exception_handler(ReviewNotFoundException, review_not_found_exception_handler)
    app.add_exception_handler(InvalidReviewException, invalid_review_exception_handler)
    app.add_exception_handler(TokenExpiredException, token_expired_exception_handler)
    app.add_exception_handler(TokenInvalidException, token_invalid_exception_handler)
    app.add_exception_handler(AuthInvalidCredentialsException, auth_invalid_credentials_exception_handler)
    app.add_exception_handler(InvalidCredentialsException, invalid_credentials_exception_handler)
    app.add_exception_handler(AccountInactiveException, account_inactive_exception_handler)
    app.add_exception_handler(AccountNotFoundException, account_not_found_exception_handler)
    app.add_exception_handler(AccountPermissionDeniedException, account_permission_denied_exception_handler)
    app.add_exception_handler(UsernameAlreadyExistsException, username_exception_handler)
