"""
Application configuration
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    PROJECT_NAME: str = "Medical Calculator API"
    
    # CORS - Allow Clacky preview domains and localhost
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://3000-1bca4202989e-web.clackypaas.com",
        "https://3001-1bca4202989e-web.clackypaas.com",
    ]
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # External Integrations (optional)
    MEDICAL_DATA_API_KEY: str = ""
    ANALYTICS_API_KEY: str = ""
    FCM_SERVER_KEY: str = ""
    
    # Firebase Configuration
    FIREBASE_API_KEY: str = ""
    FIREBASE_AUTH_DOMAIN: str = ""
    FIREBASE_PROJECT_ID: str = ""
    FIREBASE_STORAGE_BUCKET: str = ""
    FIREBASE_MESSAGING_SENDER_ID: str = ""
    FIREBASE_APP_ID: str = ""
    
    class Config:
        # Look for .env in project root (parent of api directory)
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "..", ".env")
        case_sensitive = True
        extra = "ignore"  # Ignore extra env vars like EXPO_PUBLIC_*


settings = Settings()
