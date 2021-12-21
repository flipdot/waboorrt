from dependencies import current_user, authentication_required
from api.int_models import UserAccount
from fastapi import APIRouter, Depends

from api import req_models, res_models

router = APIRouter(
    prefix="/api/account",
    dependencies=[Depends(authentication_required)],
    tags=["Account"]
)


@router.get("/", response_model=res_models.UserProfile)
def profile(user: UserAccount = Depends(current_user)):
    return user.profile


@router.put("/", response_model=res_models.UserProfile)
def update_profile(profile: req_models.UserProfile, user: UserAccount = Depends(current_user)):
    return user.profile
