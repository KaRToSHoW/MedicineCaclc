"""
Profile API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.firebase_auth import get_current_user_firebase
from app.models import User
from app.schemas import UserResponse, ProfileUpdate

router = APIRouter()


@router.get("/profiles/me", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user_firebase)):
    """Get current user profile"""
    return current_user


@router.patch("/profiles/me", response_model=UserResponse)
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db)
):
    """Update current user profile"""
    if profile_data.name is not None:
        current_user.name = profile_data.name
    
    if profile_data.email is not None:
        current_user.email = profile_data.email
    
    await db.commit()
    await db.refresh(current_user)
    
    return current_user
