from typing import Optional

from pydantic import BaseModel


class UserProfile(BaseModel):
    ssh_public_key: Optional[str]
    rc3_identity: Optional[str]
    username: str


class ChangeUserProfile(BaseModel):
    ssh_public_key: Optional[str]
