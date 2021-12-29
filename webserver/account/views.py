from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import schemas
from dependencies import current_user, authentication_required, pg_session
from fastapi import APIRouter, Depends, HTTPException, status
from models import UserModel

from .schemas import UserProfile, ChangeUserProfile

router = APIRouter(
    prefix="/api/account",
    dependencies=[Depends(authentication_required)],
    tags=["Account"]
)


@router.get("/", response_model=UserProfile)
def profile(
        user: schemas.UserSchema = Depends(current_user),
        db: Session = Depends(pg_session)
):
    user_profile: UserModel = db.query(UserModel).filter(UserModel.id == user.user_id).one()
    return UserProfile(
        ssh_public_key=user_profile.ssh_public_key,
        rc3_identity=user_profile.rc3_identity,
        username=user_profile.username,
    )


@router.put("/", response_model=UserProfile)
def update_profile(
        profile: ChangeUserProfile,
        user: schemas.UserSchema = Depends(current_user),
        db: Session = Depends(pg_session),
):
    user_profile: UserModel = db.query(UserModel).filter(UserModel.id == user.user_id).one()
    user_profile.ssh_public_key = profile.ssh_public_key
    try:
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Couldn't save data. SSH Key might already be assigned to another account."
        )
    db.refresh(user_profile)
    return UserProfile(
        ssh_public_key=user_profile.ssh_public_key,
        rc3_identity=user_profile.rc3_identity,
        username=user_profile.username,
    )
