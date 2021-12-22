from typing import Optional

from pydantic import BaseModel

from models import UserModel


class UserSchema(BaseModel):
    """
    Server side representation of the user from a web request.
    """
    user_id: int
    user: Optional[UserModel]
    is_anonymous: bool
