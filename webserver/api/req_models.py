"""
Request models. Used for validating user input
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class RepositoryTemplateName(str, Enum):
    python = "python"
    csharp = "c-sharp"
    golang = "golang"


class LegacyUserAccount(BaseModel):
    username: str
    template: RepositoryTemplateName
    pubkey: str


class UserProfile(BaseModel):
    """
    User profile information which may be changed by the owner
    """
    ssh_public_key: Optional[str]
