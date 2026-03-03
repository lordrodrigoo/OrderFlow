#pylint: disable=redefined-outer-name
import pytest
from pydantic import ValidationError
from src.dto.request.review_request import ReviewRequest



def test_valid_review_request(valid_review_data):
    review_request = ReviewRequest(**valid_review_data)
    assert review_request.user_id == valid_review_data["user_id"]
    assert review_request.product_id == valid_review_data["product_id"]
    assert review_request.rating == valid_review_data["rating"]
    assert review_request.comment == valid_review_data["comment"]


@pytest.mark.parametrize("field,value,expected_msg", [
    # user_id
    ("user_id", None, "Input should be a valid integer"),
    ("user_id", "abc", "Input should be a valid integer"),
    ("user_id", 0, "Input should be greater than 0"),
    ("user_id", -1, "Input should be greater than 0"),
    # product_id
    ("product_id", None, "Input should be a valid integer"),
    ("product_id", "abc", "Input should be a valid integer"),
    ("product_id", 0, "Input should be greater than 0"),
    ("product_id", -1, "Input should be greater than 0"),
    # rating
    ("rating", "abc", "Input should be a valid integer"),
    ("rating", -1, "Input should be greater than or equal to 0"),
    ("rating", 6, "Input should be less than or equal to 5"),
    # comment
    ("comment", "   ", "Comment cannot be empty string"),
    ("comment", "A" * 501, "String should have at most 500 characters"),
])
def test_field_validations(valid_review_data, field, value, expected_msg):
    data = valid_review_data.copy()
    data[field] = value

    with pytest.raises(ValidationError) as exc_info:
        ReviewRequest(**data)
    assert expected_msg in str(exc_info.value)


def test_optional_fields():
    review_request = ReviewRequest(user_id=1, product_id=1)
    assert review_request.rating is None
    assert review_request.comment is None
