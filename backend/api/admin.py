from typing import Optional
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from core.database import get_db
from core.rate_limiter import get_client_ip
from db.models import User
from schemas.admin import (
    AdminUserResponse,
    UserStatusUpdateRequest,
    UserRoleUpdateRequest,
    AdminUserListResponse
)
from services.admin_service import admin_service
from api.deps import (
    get_current_admin_user,
    verify_csrf_protection
)

router = APIRouter()


@router.get("/me", response_model=AdminUserResponse)
async def get_admin_me(
    current_admin: User = Depends(get_current_admin_user)
):
    """Verify administrator session and retrieve admin profile."""
    return current_admin


@router.get("/users", response_model=AdminUserListResponse)
async def get_users_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None),
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Retrieve paginated list of all users for administrator management."""
    users, total = admin_service.list_users(db, skip=skip, limit=limit, search=search)
    return {"users": users, "total": total}


@router.patch(
    "/users/{user_id}/status",
    response_model=AdminUserResponse,
    dependencies=[Depends(verify_csrf_protection)]
)
async def update_user_status(
    user_id: int,
    req: UserStatusUpdateRequest,
    request: Request,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Suspend or restore a user account. Admins cannot deactivate themselves."""
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent")
    updated_user = admin_service.update_user_status(
        db,
        target_user_id=user_id,
        is_active=req.is_active,
        current_admin=current_admin,
        client_ip=client_ip,
        user_agent=user_agent
    )
    return updated_user


@router.patch(
    "/users/{user_id}/role",
    response_model=AdminUserResponse,
    dependencies=[Depends(verify_csrf_protection)]
)
async def update_user_role(
    user_id: int,
    req: UserRoleUpdateRequest,
    request: Request,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update role between user and admin. Admins cannot demote themselves."""
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent")
    updated_user = admin_service.update_user_role(
        db,
        target_user_id=user_id,
        new_role=req.role,
        current_admin=current_admin,
        client_ip=client_ip,
        user_agent=user_agent
    )
    return updated_user
