from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str


class RepositoryTemplateName(str, Enum):
    python = "python"
    csharp = "csharp"
    golang = "golang"


class LegacyUserAccount(BaseModel):
    username: str
    template: RepositoryTemplateName
    pubkey: str

class LoginResponse(BaseModel):
    session_id: UUID
