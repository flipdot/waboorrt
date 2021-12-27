from sqlalchemy.orm import Session
from sqlalchemy import and_
from starlette import status

from dependencies import pg_session, api_authentication_required
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse

from models import UserModel, RepositoryModel
from schemas import HTTPErrorSchema
from .schemas import UserSchema, CheckRepositoryPermissionSchema, RepositoryPermissionsSchema

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
    return UserSchema(id=user.id)


@router.post("/query/check-repository-permissions", response_model=RepositoryPermissionsSchema)
def get_repo_permissions(form: CheckRepositoryPermissionSchema, db: Session = Depends(pg_session)):
    has_access = db.query(db.query(RepositoryModel).filter(
        and_(RepositoryModel.name == form.repository_name,
             RepositoryModel.owner_id == form.user_id)
    ).exists()).scalar()
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
