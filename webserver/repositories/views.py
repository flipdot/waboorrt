import logging
from typing import List
from uuid import UUID

import requests
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select

from constants import GITSERVER_HOST, GITSERVER_HTTP_PORT
from dependencies import current_user, authentication_required, pg_session
from fastapi import APIRouter, Depends, HTTPException, status
from models import RepositoryModel, UserModel
from schemas import UserSchema

from .schemas import RepositorySchema, CreateRepositorySchema

logger = logging.getLogger(__name__)

MAX_REPOS = 3

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


@router.post("/", response_model=RepositorySchema)
def create_repository(form: CreateRepositorySchema, db: Session = Depends(pg_session), user: UserSchema = Depends(current_user)):
    select(RepositoryModel)
    number_repos = db.query(RepositoryModel).filter(RepositoryModel.owner_id == user.user_id).count()
    if number_repos >= MAX_REPOS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You may not create more than {MAX_REPOS} repositories!"
        )
    user_profile: UserModel = db.query(UserModel).filter(UserModel.id == user.user_id).one()
    repo = RepositoryModel(owner_id=user.user_id, name=f"{user_profile.username}/{form.name}")
    db.add(repo)
    try:
        db.flush()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unable to create repo. Duplicate name?"
        )
    db.refresh(repo)
    res = requests.post(f"http://{GITSERVER_HOST}:{GITSERVER_HTTP_PORT}/repos", json={
        "id": repo.name,
        "template": form.template,
    })
    if res.status_code != status.HTTP_200_OK:
        logger.warning(res.content)
        logger.error(f"Bad response {res.status_code} from {GITSERVER_HOST}:{GITSERVER_HTTP_PORT}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create git repo."
            )
    db.commit()
    return RepositorySchema(id=repo.id, name=repo.name)


@router.delete("/{repo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_repository(repo_id: UUID, db: Session = Depends(pg_session), user: UserSchema = Depends(current_user)):
    n_deleted = db.query(RepositoryModel).filter(
        RepositoryModel.owner_id == user.user_id,
        RepositoryModel.id == repo_id,
    ).delete()
    if n_deleted <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such repository")
    db.commit()
