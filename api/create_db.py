"""
Create the database if it doesn't exist
"""
import asyncio
import asyncpg


async def create_database():
    """Create the database"""
    try:
        # Connect to postgres database first (using credentials from middleware)
        conn = await asyncpg.connect(
            host='127.0.0.1',
            port=5432,
            user='postgres',
            password='WSZaTvXx',  # Updated with current middleware password
            database='postgres'
        )
        
        # Check if database exists
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = 'medical_calculator_development'"
        )
        
        if not exists:
            # Create the database
            await conn.execute('CREATE DATABASE medical_calculator_development')
            print("✓ Database 'medical_calculator_development' created successfully")
        else:
            print("✓ Database 'medical_calculator_development' already exists")
        
        await conn.close()
        return True
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(create_database())
