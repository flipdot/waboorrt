from enum import Enum
from uuid import UUID

from pydantic import BaseModel, constr


class RepositorySchema(BaseModel):
    id: UUID
    name: str


class RepositoryTemplateName(str, Enum):
    python = "python"
    csharp = "csharp"
    golang = "golang"


class CreateRepositorySchema(BaseModel):
    name: constr(regex=r"^\w+$")
    template: RepositoryTemplateName
