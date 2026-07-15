from fastapi import APIRouter

router = APIRouter()


@router.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}
