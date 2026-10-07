from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict


class AdminUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    role: str
    is_active: bool
    is_email_verified: bool
    failed_login_attempts: int
    locked_until: Optional[datetime] = None
    created_at: datetime
    last_login_at: Optional[datetime] = None


class UserStatusUpdateRequest(BaseModel):
    is_active: bool = Field(..., description="Active or suspended status")


class UserRoleUpdateRequest(BaseModel):
    role: str = Field(..., description="Role must be 'user' or 'admin'")

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        v = v.strip().lower()
        if v not in ("user", "admin"):
            raise ValueError("Role must be either 'user' or 'admin'.")
        return v


class AdminUserListResponse(BaseModel):
    users: List[AdminUserResponse]
    total: int
