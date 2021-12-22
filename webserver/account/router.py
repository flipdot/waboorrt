from sqlalchemy.orm import Session

import schemas
from dependencies import current_user, authentication_required, pg_session
from fastapi import APIRouter, Depends

from .schemas import UserProfile, ChangeUserProfile

router = APIRouter(
    prefix="/api/account",
    dependencies=[Depends(authentication_required)],
    tags=["Account"]
)


@router.get("/", response_model=UserProfile)
def profile(user: schemas.UserSchema = Depends(current_user)):
    return UserProfile(
        ssh_public_key=user.user.ssh_public_key,
        rc3_identity=user.user.rc3_identity,
        username=user.user.username,
    )


@router.put("/", response_model=UserProfile)
def update_profile(
        profile: ChangeUserProfile,
        user: schemas.UserSchema = Depends(current_user),
        db: Session = Depends(pg_session),
):
    user.user.ssh_public_key = profile.ssh_public_key
    db.commit()
    db.refresh(user.user)
    return UserProfile(
        ssh_public_key=user.user.ssh_public_key,
        rc3_identity=user.user.rc3_identity,
        username=user.user.username,
    )
