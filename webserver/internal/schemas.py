from uuid import UUID

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: UUID


class CheckRepositoryPermissionSchema(BaseModel):
    repository_name: str
    user_id: UUID


class RepositoryPermissionsSchema(BaseModel):
    read: bool
    write: bool
