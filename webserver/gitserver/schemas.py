from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str
