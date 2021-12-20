"""
Response models. Used to expose data to the public.
"""

from typing import Optional

from pydantic import BaseModel


class UserProfile(BaseModel):
    ssh_public_key: Optional[str]
    rc3_identity: Optional[str]
    username: str
