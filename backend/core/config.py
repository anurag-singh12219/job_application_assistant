import os
from typing import List, Optional, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "JobPilot AI Career Assistant"
    
    # Database
    DATABASE_URL: str = "sqlite:///./auth.db"
    
    # Security / JWT
    JWT_SECRET_KEY: str = "dev-secret-key-change-in-production-jobpilot-ai-2026-auth-token"
    JWT_ALGORITHM: str = "HS256"
    JWT_ISSUER: str = "jobpilot-ai-auth"
    JWT_AUDIENCE: str = "jobpilot-ai-app"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Cookie Configuration
    COOKIE_SECURE: bool = False  # Set to True in production (HTTPS)
    COOKIE_SAMESITE: str = "lax"  # "lax", "strict", "none"
    COOKIE_DOMAIN: Optional[str] = None
    
    # Tokens expiration
    EMAIL_VERIFICATION_EXPIRE_HOURS: int = 24
    PASSWORD_RESET_EXPIRE_HOURS: int = 1
    
    # Rate Limiting & Account Lockout
    MAX_FAILED_LOGIN_ATTEMPTS: int = 5
    ACCOUNT_LOCKOUT_MINUTES: int = 15
    RATE_LIMIT_LOGIN_PER_MINUTE: int = 10
    RATE_LIMIT_REGISTER_PER_MINUTE: int = 5
    RATE_LIMIT_PASSWORD_RESET_PER_MINUTE: int = 3
    
    # CORS
    CORS_ALLOWED_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://job-application-assistant-one.vercel.app"
    ]
    
    # Frontend URL (for email links)
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Email configuration
    EMAIL_DEV_MODE: bool = True  # In dev mode, emails are printed/logged to console safely
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = True
    EMAILS_FROM_EMAIL: str = "noreply@jobpilot.ai"
    EMAILS_FROM_NAME: str = "JobPilot AI Security"
    
    # Bootstrap First Admin (optional on startup)
    FIRST_ADMIN_EMAIL: Optional[str] = None
    FIRST_ADMIN_PASSWORD: Optional[str] = None
    FIRST_ADMIN_NAME: Optional[str] = "System Administrator"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @field_validator("CORS_ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v.strip().startswith("[") and v.strip().endswith("]"):
                import json
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"]

    def validate_production_settings(self):
        """Enforce strict security requirements when in production."""
        if self.ENVIRONMENT == "production":
            if "dev-secret" in self.JWT_SECRET_KEY:
                raise ValueError("In production, JWT_SECRET_KEY must be a strong production secret.")
            if not self.COOKIE_SECURE:
                raise ValueError("In production, COOKIE_SECURE must be True.")


settings = Settings()
