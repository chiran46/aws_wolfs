from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Application
    app_name: str = "CarbonSakthi AI"
    app_version: str = "1.0.0"
    debug: bool = True
    api_v1_str: str = "/api/v1"
    project_name: str = "CarbonSakthi AI Backend"
    
    # Database
    database_url: str = "sqlite:///./carbonsakthi.db"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080", "http://localhost:8000"]
    
    # AWS
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    s3_bucket_name: Optional[str] = None
    
    # External APIs
    weather_api_key: Optional[str] = None
    carbon_api_key: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "carbonsakthi.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
