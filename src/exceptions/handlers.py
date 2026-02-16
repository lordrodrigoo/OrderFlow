from fastapi import FastAPI
from src.exceptions.exception_handlers_user import (
    EmailAlreadyExistsException, email_exception_handler,
    FieldRequiredException, field_required_exception_handler,
    UserNotFoundException, user_not_found_exception_handler
)
from src.exceptions.exception_handlers_address import (
    AddressAlreadyExistsException, address_already_exists_exception_handler,
    AddressNotFoundException, address_not_found_exception_handler,
    AddressPermissionDeniedException, address_permission_denied_exception_handler
)


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(EmailAlreadyExistsException, email_exception_handler)
    app.add_exception_handler(FieldRequiredException, field_required_exception_handler)
    app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
    app.add_exception_handler(AddressAlreadyExistsException, address_already_exists_exception_handler)
    app.add_exception_handler(AddressNotFoundException, address_not_found_exception_handler)
    app.add_exception_handler(AddressPermissionDeniedException, address_permission_denied_exception_handler)
