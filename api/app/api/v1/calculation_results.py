"""
Calculation Results API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any

from app.core.firebase_auth import get_current_user_firebase
from app.core.firestore import FirestoreCalculationResult
from app.schemas import CalculationResultCreate, CalculationResultResponse
from app.services.pdf_export import pdf_exporter
from app.services.external_integrations import analytics_service

router = APIRouter()


@router.get("/calculation_results", response_model=List[Dict[str, Any]])
async def get_calculation_results(
    current_user: Dict[str, Any] = Depends(get_current_user_firebase)
):
    """Get all calculation results for current user"""
    results = await FirestoreCalculationResult.get_by_user(current_user['id'])
    return results


@router.post("/calculation_results", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_calculation_result(
    calculation_data: CalculationResultCreate,
    current_user: Dict[str, Any] = Depends(get_current_user_firebase)
):
    """Create new calculation result"""
    # Save result to Firestore
    new_result = await FirestoreCalculationResult.create(
        user_id=current_user['id'],
        calculator_name=calculation_data.calculator_name,
        calculator_name_ru=calculation_data.calculator_name_ru,
        input_data=calculation_data.input_data,
        result_value=calculation_data.result_value,
        interpretation=calculation_data.interpretation
    )
    
    # Track analytics event
    analytics_service.track_calculation(
        calculator_name=calculation_data.calculator_name,
        calculator_category="medical",
        user_id=current_user['id']
    )
    
    return new_result


@router.get("/calculation_results/{result_id}", response_model=Dict[str, Any])
async def get_calculation_result(
    result_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user_firebase)
):
    """Get specific calculation result"""
    calc_result = await FirestoreCalculationResult.get_by_id(result_id, current_user['id'])
    
    if not calc_result:
        raise HTTPException(status_code=404, detail="Calculation result not found")
    
    return calc_result


@router.get("/calculation_results/{result_id}/export")
async def export_calculation_result_pdf(
    result_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user_firebase)
):
    """Export calculation result as PDF"""
    # Get calculation result from Firestore
    calc_result = await FirestoreCalculationResult.get_by_id(result_id, current_user['id'])
    
    if not calc_result:
        raise HTTPException(status_code=404, detail="Calculation result not found")
    
    # Generate PDF
    pdf_buffer = pdf_exporter.generate_result_pdf(
        calculator_name=calc_result['calculator_name'],
        calculator_category="medical",
        input_data=calc_result['input_data'],
        result_value=calc_result['result_value'],
        interpretation=calc_result.get('interpretation'),
        performed_at=calc_result['performed_at'],
        user_name=current_user.get('name', 'User')
    )
    
    # Track analytics event
    analytics_service.track_event(
        'pdf_export',
        user_id=current_user['id'],
        properties={
            'calculator_name': calc_result['calculator_name'],
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
