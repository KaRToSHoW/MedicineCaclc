"""
Fix calculation_results table by recreating it with correct columns
"""
import asyncio
from sqlalchemy import text
from app.core.database import engine, Base
from app.models import User, CalculationResult, UsageStatistic

async def fix_table():
    """Drop and recreate calculation_results table"""
    async with engine.begin() as conn:
        try:
            # Drop the old table
            await conn.execute(text("DROP TABLE IF EXISTS calculation_results CASCADE"))
            print("✓ Dropped old calculation_results table")
            
            # Create all tables (will recreate calculation_results with correct schema)
            await conn.run_sync(Base.metadata.create_all)
            print("✓ Created calculation_results table with correct columns")
            
            print("✅ Migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(fix_table())
