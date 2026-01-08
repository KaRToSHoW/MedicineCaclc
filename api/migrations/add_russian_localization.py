"""
Add Russian localization fields to calculators table
"""
import asyncio
import asyncpg


async def migrate():
    """Add Russian localization columns to calculators table"""
    conn = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        password='WSZaTvXx',
        database='medical_calculator_development'
    )
    
    try:
        # Add Russian localization columns
        await conn.execute("""
            ALTER TABLE calculators
            ADD COLUMN IF NOT EXISTS name_ru VARCHAR(255),
            ADD COLUMN IF NOT EXISTS description_ru TEXT,
            ADD COLUMN IF NOT EXISTS category_ru VARCHAR(100)
        """)
        
        print("✅ Successfully added Russian localization columns to calculators table")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        raise
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(migrate())
