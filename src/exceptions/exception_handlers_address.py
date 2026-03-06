# pylint: disable=unused-argument
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse




class AddressNotFoundException(Exception):
    def __init__(self, address_id: int):
        self.address_id = address_id
        self.message = f"Address '{address_id}' not found."
        super().__init__(self.message)


async def address_not_found_exception_handler(request: Request, exc: AddressNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder({'message': exc.message})
    )


class AddressAlreadyExistsException(Exception):
    def __init__(self, address: str):
        self.address = address
        self.message = f"Address '{address}' already exists."
        super().__init__(self.message)


async def address_already_exists_exception_handler(request: Request, exc: AddressAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=jsonable_encoder({'message': exc.message})
    )


class AddressPermissionDeniedException(Exception):
    def __init__(self, address_id: int):
        self.address_id = address_id
        self.message = f"You do not have permission to update address with ID: '{address_id}'."
        super().__init__(self.message)


async def address_permission_denied_exception_handler(request: Request, exc: AddressPermissionDeniedException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=jsonable_encoder({'message': exc.message})
    )
