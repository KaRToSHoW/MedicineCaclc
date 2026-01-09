"""
Calculation Results API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, CalculationResult
from app.schemas import CalculationResultCreate, CalculationResultResponse
from app.services.pdf_export import pdf_exporter
from app.services.external_integrations import analytics_service

router = APIRouter()


@router.get("/calculation_results", response_model=List[CalculationResultResponse])
async def get_calculation_results(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all calculation results for current user"""
    result = await db.execute(
        select(CalculationResult)
        .where(CalculationResult.user_id == current_user.id)
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
    # Save result (calculation already done on frontend)
    new_result = CalculationResult(
        user_id=current_user.id,
        calculator_name=calculation_data.calculator_name,
        calculator_name_ru=calculation_data.calculator_name_ru,
        input_data=calculation_data.input_data,
        result_value=calculation_data.result_value,
        interpretation=calculation_data.interpretation
    )
    db.add(new_result)
    await db.commit()
    await db.refresh(new_result)
    
    # Track analytics event
    analytics_service.track_calculation(
        calculator_name=calculation_data.calculator_name,
        calculator_category="medical",
        user_id=current_user.id
    )
    
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
    )
    calc_result = result.scalar_one_or_none()
    
    if not calc_result:
        raise HTTPException(status_code=404, detail="Calculation result not found")
    
    return calc_result


@router.get("/calculation_results/{result_id}/export")
async def export_calculation_result_pdf(
    result_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Export calculation result as PDF"""
    # Get calculation result
    result = await db.execute(
        select(CalculationResult)
        .where(
            CalculationResult.id == result_id,
            CalculationResult.user_id == current_user.id
        )
    )
    calc_result = result.scalar_one_or_none()
    
    if not calc_result:
        raise HTTPException(status_code=404, detail="Calculation result not found")
    
    # Generate PDF
    pdf_buffer = pdf_exporter.generate_result_pdf(
        calculator_name=calc_result.calculator_name,
        calculator_category="medical",
        input_data=calc_result.input_data,
        result_value=calc_result.result_value,
        interpretation=calc_result.interpretation,
        performed_at=calc_result.performed_at,
        user_name=f"{current_user.name or 'User'}"
    )
    
    # Track analytics event
    analytics_service.track_event(
        'pdf_export',
        user_id=current_user.id,
        properties={
            'calculator_name': calc_result.calculator_name,
            'result_id': result_id
        }
    )
    
    # Return PDF as streaming response
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="medical_calc_result_{result_id}.pdf"'
        }
    )
