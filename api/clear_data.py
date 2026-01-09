"""
Clear all calculators from database
"""
import asyncio
from sqlalchemy import delete
from app.core.database import AsyncSessionLocal
from app.models import Calculator


async def clear_calculators():
    """Delete all calculators from database"""
    async with AsyncSessionLocal() as session:
        # Delete all calculators
        await session.execute(delete(Calculator))
        await session.commit()
        print("✅ All calculators have been deleted from database")


if __name__ == "__main__":
    asyncio.run(clear_calculators())
