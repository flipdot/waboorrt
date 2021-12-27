from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select

from dependencies import current_user, authentication_required, pg_session
from fastapi import APIRouter, Depends
from models import  RepositoryModel
from schemas import UserSchema

from .schemas import RepositorySchema

router = APIRouter(
    prefix="/api/repositories",
    dependencies=[Depends(authentication_required)],
    tags=["Repositories"]
)


@router.get("/", response_model=List[RepositorySchema])
def repository_list(db: Session = Depends(pg_session), user: UserSchema = Depends(current_user)):
    query = select(RepositoryModel.id, RepositoryModel.name).where(
        RepositoryModel.owner_id == user.user_id
    )
    res = db.execute(query)
    return [
        RepositorySchema(id=r.id, name=r.name)
        for r in res
    ]
