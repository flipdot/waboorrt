from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator


class UserSchema(BaseModel):
    id: UUID
    username: str


class CheckRepositoryPermissionSchema(BaseModel):
    repository_name: str
    user_id: UUID


class RepositoryPermissionsSchema(BaseModel):
    read: bool
    write: bool


class CreateSuperuserSchema(BaseModel):
    ssh_public_key: str
    username: Optional[str]

    @validator("ssh_public_key")
    def strip_comment(cls, v):
        # Remove everything after the second space. Discards comments from ssh keys
        pubkey = " ".join(v.split(" ")[:2])
        return pubkey
