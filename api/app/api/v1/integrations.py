"""
External integrations API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from app.core.firebase_auth import get_current_user_firebase
from app.services.external_integrations import medical_data_service

router = APIRouter()


class ReferenceRangeQuery(BaseModel):
    test_name: str
    age: int
    gender: str


class ICD10SearchResponse(BaseModel):
    code: str
    description: str


@router.post("/integrations/reference-ranges")
async def get_reference_ranges(
    query: ReferenceRangeQuery,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_firebase)
):
    """Get medical reference ranges"""
    result = medical_data_service.get_reference_ranges(
        test_name=query.test_name,
        age=query.age,
        gender=query.gender
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Reference ranges not found")
    
    return result


@router.get("/integrations/icd10/search", response_model=List[ICD10SearchResponse])
async def search_icd10(
    q: str,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_firebase)
):
    """Search ICD-10 diagnostic codes"""
    if not q or len(q) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
    
    results = medical_data_service.search_icd10_codes(q)
    return results
