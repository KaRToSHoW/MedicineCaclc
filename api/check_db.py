import asyncio
from app.core.database import engine
from sqlalchemy import text

async def check_database():
    """Check database contents"""
    async with engine.connect() as conn:
        # Check calculation_results
        result = await conn.execute(text('SELECT COUNT(*) FROM calculation_results'))
        count = result.scalar()
        print(f'calculation_results: {count} records')
        
        # Check users
        result = await conn.execute(text('SELECT COUNT(*) FROM users'))
        count = result.scalar()
        print(f'users: {count} records')
        
        # Show recent calculations
        if count > 0:
            result = await conn.execute(text('''
                SELECT cr.id, cr.calculator_name, cr.result_value, cr.created_at, u.email
                FROM calculation_results cr
                JOIN users u ON cr.user_id = u.id
                ORDER BY cr.created_at DESC
                LIMIT 5
            '''))
            rows = result.fetchall()
            print('\nRecent calculations:')
            for row in rows:
                print(f'  ID: {row[0]}, Calculator: {row[1]}, Result: {row[2]}, User: {row[4]}, Time: {row[3]}')

if __name__ == '__main__':
    asyncio.run(check_database())
