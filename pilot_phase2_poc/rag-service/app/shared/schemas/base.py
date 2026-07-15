from pydantic import BaseModel


class BaseResponse(BaseModel):
    api_version: str = "v1"
