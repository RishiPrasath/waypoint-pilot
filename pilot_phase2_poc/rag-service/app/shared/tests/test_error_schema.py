from app.shared.errors.schemas import ErrorResponse
from app.shared.schemas.base import BaseResponse
from pydantic import ValidationError


def test_error_response_requires_code_and_message():
    error = ErrorResponse(error_code="bad_request", message="Invalid request")

    assert error.error_code == "bad_request"
    assert error.message == "Invalid request"


def test_base_response_exposes_default_api_version():
    response = BaseResponse()

    assert response.api_version == "v1"


def test_error_response_requires_error_code_and_message():
    try:
        ErrorResponse(message="Invalid request")
    except ValidationError as exc:
        assert "error_code" in str(exc)
    else:
        raise AssertionError("expected error_code validation to fail")

    try:
        ErrorResponse(error_code="bad_request")
    except ValidationError as exc:
        assert "message" in str(exc)
    else:
        raise AssertionError("expected message validation to fail")
