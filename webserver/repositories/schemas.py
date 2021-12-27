from uuid import UUID

from pydantic import BaseModel


class RepositorySchema(BaseModel):
    id: UUID
    name: str
