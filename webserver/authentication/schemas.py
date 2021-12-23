from enum import Enum

from pydantic import BaseModel


class RepositoryTemplateName(str, Enum):
    python = "python"
    csharp = "c-sharp"
    golang = "golang"


class LegacyUserAccount(BaseModel):
    username: str
    template: RepositoryTemplateName
    pubkey: str
