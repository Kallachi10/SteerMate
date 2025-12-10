"""User profile router."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import UserResponse
from schemas.profile import ProfileUpdate
from utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile."""
    return current_user


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user's profile."""
    if profile_data.name is not None:
        current_user.name = profile_data.name
    
    await db.commit()
    await db.refresh(current_user)
    
    return current_user
