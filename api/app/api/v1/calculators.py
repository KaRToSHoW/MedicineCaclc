"""
Calculators API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models import Calculator
from app.schemas import CalculatorResponse

router = APIRouter()


@router.get("/calculators", response_model=List[CalculatorResponse])
async def get_calculators(db: AsyncSession = Depends(get_db)):
    """Get all calculators"""
    result = await db.execute(select(Calculator))
    calculators = result.scalars().all()
    return calculators


@router.get("/calculators/{calculator_id}", response_model=CalculatorResponse)
async def get_calculator(calculator_id: int, db: AsyncSession = Depends(get_db)):
    """Get calculator by ID"""
    result = await db.execute(
        select(Calculator).where(Calculator.id == calculator_id)
    )
    calculator = result.scalar_one_or_none()
    
    if not calculator:
        raise HTTPException(status_code=404, detail="Calculator not found")
    
    return calculator
