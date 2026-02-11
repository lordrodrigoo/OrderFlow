import re
from pydantic import BaseModel, Field, field_validator

VALID_UF ={
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
}

class AddressRequest(BaseModel):
    user_id: int = Field(
        ...,
        description="ID of the user to whom the address belongs"
    )


    street: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="street must be between 3 and 100 characters",
    )

    number: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="number must be between 1 and 10 characters",
    )

    complement: str = Field(
        None,
        max_length=50,
        description="complement must be up to 50 characters",
    )

    neighborhood: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="neighborhood must be between 3 and 50 characters",
    )

    city: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="city must be between 3 and 50 characters",
    )

    state: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="state must be 2 characters (UF)",
    )

    zip_code: str = Field(
        ...,
        min_length=5,
        max_length=10,
        description="zip code must be between 5 and 10 characters",
    )

    is_default: bool = True

    @field_validator("number")
    @classmethod
    def validate_number(cls, number: str) -> str:
        try:
            num = int(number)
            if num < 0:
                raise ValueError("number must be a positive integer")
        except ValueError:
            pass
        return number


    @field_validator("zip_code")
    @classmethod
    def validate_zip_code(cls, zip_code: str) -> str:
        cep_digits = re.sub(r'\D', '', zip_code)
        if len(cep_digits) != 8:
            raise ValueError("zip code invalid.")
        return f"{cep_digits[:5]}-{cep_digits[5:]}"


    @field_validator("state")
    @classmethod
    def validate_state(cls, state: str) -> str:
        state = state.upper()
        if state not in VALID_UF:
            raise ValueError("state invalid.")
        return state


    @field_validator(
            "street",
            "neighborhood",
            "city",
            "complement",
            "state"
        )
    @classmethod
    def validate_text_fields(cls, v: str) -> str:
        if not re.match(r'^[A-Za-zÀ-ÿ0-9\s]+$', v):
            raise ValueError('Fields contains invalid characters.')
        return v
