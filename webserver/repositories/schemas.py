from uuid import UUID

from pydantic import BaseModel, constr


class RepositorySchema(BaseModel):
    id: UUID
    name: str


class CreateRepositorySchema(BaseModel):
    name: constr(regex=r"^\w+$")
