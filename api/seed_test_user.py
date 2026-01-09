#!/usr/bin/env python3
"""
Seed test user for development
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import engine, Base
from app.models import User
from app.core.security import get_password_hash


async def seed_test_user():
    """Create test user: test@example.com / password123"""
    
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSession(engine) as session:
        # Check if user already exists
        result = await session.execute(
            select(User).where(User.email == "test@example.com")
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print("✅ Test user already exists: test@example.com")
            return
        
        # Create test user
        test_user = User(
            email="test@example.com",
            name="Test User",
            password_digest=get_password_hash("password123")
        )
        
        session.add(test_user)
        await session.commit()
        
        print("✅ Created test user:")
        print("   Email: test@example.com")
        print("   Password: password123")
        print("   Name: Test User")


if __name__ == "__main__":
    asyncio.run(seed_test_user())
