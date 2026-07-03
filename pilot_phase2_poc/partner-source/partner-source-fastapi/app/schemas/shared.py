from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str


class ReadinessChecks(BaseModel):
    persistence: str
    seedData: str


class ReadinessResponse(BaseModel):
    status: str
    service: str
    checks: ReadinessChecks