from fastapi import APIRouter

from app.repositories.drivers import InMemoryDriverRepository
from app.schemas.auth import DemoLoginRequest, DemoLoginResponse
from app.security.demo_login import DemoLoginService
from app.state import get_store

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post("/demo-login", response_model=DemoLoginResponse)
def demo_login(request: DemoLoginRequest) -> DemoLoginResponse:
    store = get_store()
    service = DemoLoginService(InMemoryDriverRepository(store))
    return service.login(request)
