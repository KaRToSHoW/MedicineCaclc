"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import secrets

from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user
)
from app.models import User, Session
from app.schemas import UserCreate, UserLogin, SessionResponse, UserResponse

router = APIRouter()


@router.post("/registrations", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        password_digest=hashed_password
    )
    db.add(new_user)
    await db.flush()
    
    # Create session
    session_token = secrets.token_urlsafe(32)
    new_session = Session(
        user_id=new_user.id,
        session_token=session_token
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_user)
    
    # Create JWT token
    access_token = create_access_token(data={"sub": session_token})
    
    return {
        "session_token": access_token,
        "user": new_user
    }


@router.post("/sessions", response_model=SessionResponse)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login user"""
    # Find user
    result = await db.execute(
        select(User).where(User.email == credentials.email)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.password_digest):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create session
    session_token = secrets.token_urlsafe(32)
    new_session = Session(
        user_id=user.id,
        session_token=session_token
    )
    db.add(new_session)
    await db.commit()
    
    # Create JWT token
    access_token = create_access_token(data={"sub": session_token})
    
    return {
        "session_token": access_token,
        "user": user
    }


@router.delete("/sessions")
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Logout user (delete all sessions)"""
    await db.execute(
        select(Session).where(Session.user_id == current_user.id)
    )
    # Delete all user sessions
    sessions_result = await db.execute(
        select(Session).where(Session.user_id == current_user.id)
    )
    sessions = sessions_result.scalars().all()
    
    for session in sessions:
        await db.delete(session)
    
    await db.commit()
    
    return {"message": "Logged out successfully"}
