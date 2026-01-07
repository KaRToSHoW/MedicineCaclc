"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Session schemas
class SessionResponse(BaseModel):
    session_token: str
    user: UserResponse


# Calculator schemas
class CalculatorBase(BaseModel):
    name: str
    description: Optional[str] = None
    formula: str
    category: str
    input_fields: List[Dict[str, Any]]
    interpretation_rules: Optional[List[Dict[str, Any]]] = None


class CalculatorCreate(CalculatorBase):
    pass


class CalculatorResponse(CalculatorBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Calculation Result schemas
class CalculationResultCreate(BaseModel):
    calculator_id: int
    input_data: Dict[str, Any]


class CalculationResultResponse(BaseModel):
    id: int
    user_id: int
    calculator_id: int
    input_data: Dict[str, Any]
    result_value: float
    interpretation: Optional[str] = None
    performed_at: datetime
    calculator: Optional[CalculatorResponse] = None
    
    class Config:
        from_attributes = True


# Profile schemas
class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


# Health check
class HealthResponse(BaseModel):
    status: str = "healthy"
