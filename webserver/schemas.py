from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserSchema(BaseModel):
    """
    Server side representation of the user from a web request.
    """
    user_id: Optional[UUID]
    is_anonymous: bool


class HTTPErrorSchema(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised"},
        }
