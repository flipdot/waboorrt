from pydantic import BaseModel


class UserSchema(BaseModel):
    """
    Server side representation of the user from a web request.
    """
    user_id: int
    is_anonymous: bool


class HTTPErrorSchema(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised"},
        }