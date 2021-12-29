from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str


class LoginResponse(BaseModel):
    session_id: UUID


class OAuthProvider(str, Enum):
    rc3 = "rc3"
    local = "local"
