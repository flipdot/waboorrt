from uuid import UUID

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: UUID
