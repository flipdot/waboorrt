"""
Internal data models. Not meant for direct API exposure
"""

from pydantic import BaseModel
from api import res_models


class UserAccount(BaseModel):
    """
    Server side representation of the user from a web request.
    """
    user_id: int
    is_anonymous: bool

    @property
    def profile(self) -> res_models.UserProfile:
        return res_models.UserProfile(
            ssh_public_key="ssh-rsa AAAAB3n someone@example.com",
            rc3_identity="FooBar",
            username="foobar",
        )
