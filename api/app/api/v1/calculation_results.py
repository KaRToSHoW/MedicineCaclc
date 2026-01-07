"""
Calculation Results API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
import re

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Calculator, CalculationResult
from app.schemas import CalculationResultCreate, CalculationResultResponse

router = APIRouter()


def evaluate_formula(formula: str, input_data: dict) -> float:
    """Evaluate calculator formula with input data"""
    # Replace variable placeholders with values
    expression = formula
    for key, value in input_data.items():
        expression = expression.replace(f"{{{key}}}", str(value))
    
    try:
        # Safely evaluate mathematical expression
        result = eval(expression, {"__builtins__": {}}, {})
        return float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error evaluating formula: {str(e)}"
        )


def interpret_result(result_value: float, interpretation_rules: list) -> str:
    """Interpret result based on rules"""
    if not interpretation_rules:
        return "Result calculated successfully"
    
    for rule in interpretation_rules:
        condition = rule.get("condition", "")
        
        if not condition:
            return rule.get("interpretation", "")
        
        try:
            # Parse condition and check if result matches
            if "=" in condition and ">=" not in condition and "<=" not in condition:
                # Exact match
                expected = float(condition.split("=")[1].strip())
                if abs(result_value - expected) < 0.01:
                    return rule.get("interpretation", "")
            
            elif ">=" in condition and "and" in condition and "<" in condition:
                # Range: >= X and < Y
                parts = condition.split("and")
                min_val = float(parts[0].split(">=")[1].strip())
                max_val = float(parts[1].split("<")[1].strip())
                if min_val <= result_value < max_val:
                    return rule.get("interpretation", "")
            
            elif "<=" in condition:
                # Less than or equal
                max_val = float(condition.split("<=")[1].strip())
                if result_value <= max_val:
                    return rule.get("interpretation", "")
            
            elif ">=" in condition:
                # Greater than or equal
                min_val = float(condition.split(">=")[1].strip())
                if result_value >= min_val:
                    return rule.get("interpretation", "")
            
            elif "<" in condition:
                # Less than
                max_val = float(condition.split("<")[1].strip())
                if result_value < max_val:
                    return rule.get("interpretation", "")
            
            elif ">" in condition:
                # Greater than
                min_val = float(condition.split(">")[1].strip())
                if result_value > min_val:
                    return rule.get("interpretation", "")
        
        except Exception:
            continue
    
    return "Result calculated"


@router.get("/calculation_results", response_model=List[CalculationResultResponse])
async def get_calculation_results(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all calculation results for current user"""
    result = await db.execute(
        select(CalculationResult)
        .where(CalculationResult.user_id == current_user.id)
        .options(selectinload(CalculationResult.calculator))
        .order_by(CalculationResult.performed_at.desc())
    )
    results = result.scalars().all()
    return results


@router.post("/calculation_results", response_model=CalculationResultResponse, status_code=status.HTTP_201_CREATED)
async def create_calculation_result(
    calculation_data: CalculationResultCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create new calculation result"""
    # Get calculator
    result = await db.execute(
        select(Calculator).where(Calculator.id == calculation_data.calculator_id)
    )
    calculator = result.scalar_one_or_none()
    
    if not calculator:
        raise HTTPException(status_code=404, detail="Calculator not found")
    
    # Calculate result
    result_value = evaluate_formula(calculator.formula, calculation_data.input_data)
    
    # Interpret result
    interpretation = interpret_result(result_value, calculator.interpretation_rules or [])
    
    # Save result
    new_result = CalculationResult(
        user_id=current_user.id,
        calculator_id=calculator.id,
        input_data=calculation_data.input_data,
        result_value=result_value,
        interpretation=interpretation
    )
    db.add(new_result)
    await db.commit()
    await db.refresh(new_result)
    
    # Load calculator relationship
    await db.refresh(new_result, ["calculator"])
    
    return new_result


@router.get("/calculation_results/{result_id}", response_model=CalculationResultResponse)
async def get_calculation_result(
    result_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific calculation result"""
    result = await db.execute(
        select(CalculationResult)
        .where(
            CalculationResult.id == result_id,
            CalculationResult.user_id == current_user.id
        )
        .options(selectinload(CalculationResult.calculator))
    )
    calc_result = result.scalar_one_or_none()
    
    if not calc_result:
        raise HTTPException(status_code=404, detail="Calculation result not found")
    
    return calc_result
