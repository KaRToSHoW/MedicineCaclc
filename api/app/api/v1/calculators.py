"""
Calculators API endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import Calculator
from app.schemas import CalculatorResponse

router = APIRouter(prefix="/calculators")


@router.get("", response_model=List[CalculatorResponse])
async def get_calculators(
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all calculators, optionally filtered by category
    """
    try:
        query = select(Calculator)
        
        if category:
            query = query.where(Calculator.category == category)
        
        result = await db.execute(query)
        calculators = result.scalars().all()
        
        return calculators
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{calculator_id}", response_model=CalculatorResponse)
async def get_calculator(
    calculator_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific calculator by ID
    """
    try:
        query = select(Calculator).where(Calculator.id == calculator_id)
        result = await db.execute(query)
        calculator = result.scalar_one_or_none()
        
        if not calculator:
            raise HTTPException(status_code=404, detail="Calculator not found")
        
        return calculator
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
