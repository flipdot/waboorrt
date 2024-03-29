from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from starlette import status
import randomname

from dependencies import pg_session, api_authentication_required
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse

from models import UserModel, RepositoryModel
from schemas import HTTPErrorSchema
from .schemas import UserSchema, CheckRepositoryPermissionSchema, RepositoryPermissionsSchema, CreateSuperuserSchema

router = APIRouter(
    prefix="/api/internal",
    dependencies=[Depends(api_authentication_required)],
    tags=["Internal"]
)


@router.get("/users/by-ssh-key/{ssh_public_key:path}", response_model=UserSchema, responses={
    status.HTTP_404_NOT_FOUND: {"model": HTTPErrorSchema}
})
def get_user_by_public_key(ssh_public_key: str, db: Session = Depends(pg_session)):
    user = db.query(UserModel).filter(UserModel.ssh_public_key == ssh_public_key).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return UserSchema(id=user.id, username=user.username)


@router.post("/users", response_model=UserSchema)
def create_super_user(form: CreateSuperuserSchema, db: Session = Depends(pg_session)):
    """
    Creates a superuser account.
    A superuser can access any repository, but doesn't have an own repo.
    Username is optional, default is a random username
    """
    if form.username:
        username = form.username
    else:
        while True:
            # failsafe username generation in case of picked name already exists
            # (I don't know how many combinations the randomname library provides)
            username = randomname.get_name()
            if not user_exists(db, username):
                break
    user = UserModel(username=username, ssh_public_key=form.ssh_public_key, is_superuser=True)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Couldn't save data. SSH Key might already be assigned to another account."
        )
    db.refresh(user)
    return UserSchema(id=user.id, username=user.username)


@router.post("/query/check-repository-permissions", response_model=RepositoryPermissionsSchema)
def get_repo_permissions(form: CheckRepositoryPermissionSchema, db: Session = Depends(pg_session)):
    has_access = db.query(
        db.query(RepositoryModel, UserModel).filter(
            and_(
                RepositoryModel.name == form.repository_name,
                or_(
                     RepositoryModel.owner_id == form.user_id,
                     db.query(UserModel).with_entities(UserModel.is_superuser).filter(UserModel.id == form.user_id)
                )
            )
        ).exists()
    ).scalar()
    return RepositoryPermissionsSchema(
        read=has_access,
        write=has_access,
    )


@router.get("/auth_test", response_class=PlainTextResponse)
def auth_test():
    """
    Always returns "ok" if appropriate authentication was provided
    """
    return "ok"


def user_exists(db: Session, username: str):
    return db.query(db.query(UserModel).filter(UserModel.username == username).exists()).scalar()
