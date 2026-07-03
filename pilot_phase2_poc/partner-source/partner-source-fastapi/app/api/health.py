from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.schemas.shared import HealthResponse, ReadinessChecks, ReadinessResponse
from app.services.readiness import ReadinessService

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse(status="UP", service="partner-source")



@router.get("/ready", response_model=ReadinessResponse)
def get_readiness() -> ReadinessResponse | JSONResponse:
    checks = ReadinessService().check()
    ready = checks["persistence"] == "UP" and checks["seedData"] == "UP"
    body = ReadinessResponse(
        status="READY" if ready else "NOT_READY",
        service="partner-source",
        checks=ReadinessChecks(**checks),
    )

    if ready:
        return body

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=body.model_dump(),
    )