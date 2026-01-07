"""
Database models
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.core.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255))
    password_digest = Column(String(255), nullable=False)
    role = Column(String(50), default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    calculation_results = relationship("CalculationResult", back_populates="user", cascade="all, delete-orphan")


class Session(Base):
    """Session model for authentication"""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    session_token = Column(String(255), unique=True, index=True, nullable=False)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="sessions")


class Calculator(Base):
    """Calculator model"""
    __tablename__ = "calculators"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    formula = Column(Text, nullable=False)
    category = Column(String(100), index=True)
    input_fields = Column(JSON, nullable=False)
    interpretation_rules = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    calculation_results = relationship("CalculationResult", back_populates="calculator")


class CalculationResult(Base):
    """Calculation result model"""
    __tablename__ = "calculation_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    calculator_id = Column(Integer, ForeignKey("calculators.id", ondelete="CASCADE"), nullable=False)
    input_data = Column(JSON, nullable=False)
    result_value = Column(Float, nullable=False)
    interpretation = Column(Text)
    performed_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="calculation_results")
    calculator = relationship("Calculator", back_populates="calculation_results")


class UsageStatistic(Base):
    """Usage statistics model"""
    __tablename__ = "usage_statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    calculator_id = Column(Integer, ForeignKey("calculators.id", ondelete="CASCADE"))
    action = Column(String(100))
    meta_data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
