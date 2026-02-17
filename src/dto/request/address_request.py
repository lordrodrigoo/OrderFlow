import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator


VALID_UF ={
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
}

LETTERS_AND_NUMBERS = re.compile(r'^[A-Za-zÀ-ÿ0-9\s]+$')
LETTERS_ONLY = re.compile(r'^[A-Za-zÀ-ÿ\s]+$')
ALPHANUMERIC_EXTENDED = re.compile(r'^[\w\s\-]+$')

class AddressRequest(BaseModel):
    user_id: int = Field(
        ...,
        description="ID of the user to whom the address belongs"
    )


    street: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Street name, ex: 'AV Paulista'",
    )

    number: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Number of the address, ex: '123'",
    )

    complement: Optional[str] = Field(
        None,
        max_length=50,
        description="Complement of the address, ex: 'Apt 101'",
    )

    neighborhood: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Neighborhood ex: 'Centro'",
    )

    city: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="City name, ex: 'São Paulo'",
    )

    state: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="State must be 2 characters (UF), ex: 'SP'",
    )

    zip_code: str = Field(
        ...,
        description="Zip code ex: '01001-000'",
    )

    is_default: bool = True


    @field_validator("street")
    @classmethod
    def validate_street(cls, value: str) -> str:
        if not LETTERS_AND_NUMBERS.match(value):
            raise ValueError("street must contain letters or numbers")
        return value


    @field_validator("number")
    @classmethod
    def validate_number(cls, value: str) -> str:
        if not ALPHANUMERIC_EXTENDED.match(value) or not value.strip():
            raise ValueError("number must contain letters, numbers, or hyphens")
        return value


    @field_validator("complement")
    @classmethod
    def validate_complement(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not ALPHANUMERIC_EXTENDED.match(value):
            raise ValueError("complement must contain letters, numbers, or hyphens.")
        return value


    @field_validator("neighborhood")
    @classmethod
    def validate_neighborhood(cls, value: str) -> str:
        if not LETTERS_ONLY.match(value):
            raise ValueError("neighborhood must contain only letters.")
        return value


    @field_validator("city")
    @classmethod
    def validate_city(cls, value: str) -> str:
        if not LETTERS_ONLY.match(value):
            raise ValueError("city must contain only letters.")
        return value


    @field_validator("state")
    @classmethod
    def validate_state(cls, value: str) -> str:
        if value.upper() not in VALID_UF:
            raise ValueError("invalid Brazilian state (UF).")
        return value.upper()


    @field_validator("zip_code")
    @classmethod
    def validate_zip_code(cls, value: str) -> str:
        digits = re.sub(r'\D', '', value)
        if len(digits) != 8:
            raise ValueError("zip code must have exactly 8 digits.")
        return f"{digits[:5]}-{digits[5:]}"
