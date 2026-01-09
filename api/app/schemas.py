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


# Calculation Result schemas
class CalculationResultCreate(BaseModel):
    calculator_name: str
    calculator_name_ru: Optional[str] = None
    input_data: Dict[str, Any]
    result_value: float
    interpretation: Optional[str] = None


class CalculationResultResponse(BaseModel):
    id: int
    user_id: int
    calculator_name: str
    calculator_name_ru: Optional[str] = None
    input_data: Dict[str, Any]
    result_value: float
    interpretation: Optional[str] = None
    performed_at: datetime
    
    class Config:
        from_attributes = True


# Profile schemas
class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


# Health check
class HealthResponse(BaseModel):
    status: str = "healthy"
