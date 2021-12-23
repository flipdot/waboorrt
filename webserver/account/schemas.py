from typing import Optional

from pydantic import BaseModel, validator


class UserProfile(BaseModel):
    ssh_public_key: Optional[str]
    rc3_identity: Optional[str]
    username: str


class ChangeUserProfile(BaseModel):
    ssh_public_key: Optional[str]

    @validator("ssh_public_key")
    def strip_comment(cls, v):
        # Remove everything after the second space. Discards comments from ssh keys
        pubkey = " ".join(v.split(" ")[:2])
        return pubkey
