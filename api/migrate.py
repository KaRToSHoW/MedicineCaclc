"""
Database migration: Remove calculators table, update calculation_results
"""
import asyncio
from sqlalchemy import text
from app.core.database import AsyncSessionLocal

async def migrate():
    """Run migration"""
    async with AsyncSessionLocal() as db:
        try:
            # Drop calculators table if exists
            await db.execute(text("DROP TABLE IF EXISTS calculators CASCADE"))
            
            # Check if calculation_results exists
            result = await db.execute(text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'calculation_results')"
            ))
            table_exists = result.scalar()
            
            if table_exists:
                # Drop old calculation_results table
                await db.execute(text("DROP TABLE IF EXISTS calculation_results CASCADE"))
            
            # Create new calculation_results table
            await db.execute(text("""
                CREATE TABLE calculation_results (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    calculator_name VARCHAR(255) NOT NULL,
                    calculator_name_ru VARCHAR(255),
                    input_data JSON NOT NULL,
                    result_value FLOAT NOT NULL,
                    interpretation TEXT,
                    performed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create index
            await db.execute(text(
                "CREATE INDEX ix_calculation_results_calculator_name ON calculation_results(calculator_name)"
            ))
            
            # Update usage_statistics if it exists
            result = await db.execute(text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'usage_statistics')"
            ))
            stats_exists = result.scalar()
            
            if stats_exists:
                # Check if calculator_id column exists
                result = await db.execute(text(
                    "SELECT EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'usage_statistics' AND column_name = 'calculator_id')"
                ))
                col_exists = result.scalar()
                
                if col_exists:
                    # Drop calculator_id column, add calculator_name
                    await db.execute(text("ALTER TABLE usage_statistics DROP COLUMN IF EXISTS calculator_id"))
                    await db.execute(text("ALTER TABLE usage_statistics ADD COLUMN IF NOT EXISTS calculator_name VARCHAR(255)"))
            
            await db.commit()
            print("✅ Migration completed successfully!")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ Migration failed: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(migrate())
