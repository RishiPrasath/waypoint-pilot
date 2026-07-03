from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.errors.exceptions import InvalidRequestError, PartnerSourceError
from app.schemas.errors import ProblemDetail


def _correlation_id(request: Request) -> str:
    return request.headers.get("X-Correlation-Id", "local-dev")


def _problem_type(error_code: str) -> str:
    problem_slug = error_code.lower().replace("_", "-")
    return f"https://waypoint.local/problems/{problem_slug}"


def _problem(request: Request, error: PartnerSourceError) -> ProblemDetail:
    return ProblemDetail(
        type=_problem_type(error.error_code),
        title=error.title,
        status=error.status_code,
        detail=error.detail,
        instance=str(request.url.path),
        errorCode=error.error_code,
        correlationId=_correlation_id(request),
    )


async def partner_source_error_handler(request: Request, exc: PartnerSourceError) -> JSONResponse:
    problem = _problem(request, exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=problem.model_dump(),
        media_type="application/problem+json",
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    error = InvalidRequestError("Request validation failed.")
    problem = _problem(request, error)
    return JSONResponse(
        status_code=400,
        content=problem.model_dump(),
        media_type="application/problem+json",
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(PartnerSourceError, partner_source_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
