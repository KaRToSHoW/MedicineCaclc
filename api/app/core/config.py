"""
Application configuration
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    PROJECT_NAME: str = "Medical Calculator API"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/medical_calculator_development"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # External Integrations (optional)
    MEDICAL_DATA_API_KEY: str = ""
    ANALYTICS_API_KEY: str = ""
    FCM_SERVER_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra env vars like EXPO_PUBLIC_*


settings = Settings()
