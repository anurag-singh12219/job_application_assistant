from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, ConfigDict
from core.security import validate_password_strength


class UserRegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, max_length=128, description="Strong password")
    confirm_password: str = Field(..., min_length=8, max_length=128, description="Confirm password")
    accept_terms: Optional[bool] = Field(default=False, description="Accept terms and privacy policy")

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("full_name")
    @classmethod
    def clean_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Full name must be at least 2 characters.")
        return v

    @model_validator(mode="after")
    def validate_passwords_match_and_strength(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        is_valid, error_msg = validate_password_strength(self.password)
        if not is_valid:
            raise ValueError(error_msg or "Password is not strong enough.")
        return self


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)
    remember_me: Optional[bool] = False

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=16, description="Reset token from email")
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)

    @model_validator(mode="after")
    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        is_valid, error_msg = validate_password_strength(self.password)
        if not is_valid:
            raise ValueError(error_msg or "Password is not strong enough.")
        return self


class VerifyEmailRequest(BaseModel):
    token: str = Field(..., min_length=16, description="Verification token from email")


class ResendVerificationRequest(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_new_password: str = Field(..., min_length=8, max_length=128)

    @model_validator(mode="after")
    def validate_new_passwords(self):
        if self.new_password != self.confirm_new_password:
            raise ValueError("New passwords do not match.")
        if self.current_password == self.new_password:
            raise ValueError("New password must be different from current password.")
        is_valid, error_msg = validate_password_strength(self.new_password)
        if not is_valid:
            raise ValueError(error_msg or "New password is not strong enough.")
        return self


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    role: str
    is_active: bool
    is_email_verified: bool
    created_at: datetime
    last_login_at: Optional[datetime] = None


class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None


class AuthSuccessResponse(BaseModel):
    message: str
    user: UserResponse
    csrf_token: Optional[str] = None
    access_token: Optional[str] = None
