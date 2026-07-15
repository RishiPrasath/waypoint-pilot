from app.shared.errors.schemas import ErrorResponse
from app.shared.schemas.base import BaseResponse


def test_error_response_requires_code_and_message():
    error = ErrorResponse(error_code="bad_request", message="Invalid request")

    assert error.error_code == "bad_request"
    assert error.message == "Invalid request"


def test_base_response_exposes_default_api_version():
    response = BaseResponse()

    assert response.api_version == "v1"
