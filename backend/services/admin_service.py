import logging
from typing import List, Optional, Tuple
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from core.security import get_password_hash
from db.models import User
from services.auth_service import AuthService, utc_now

logger = logging.getLogger("auth.admin")


class AdminService:
    @staticmethod
    def list_users(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        search: Optional[str] = None
    ) -> Tuple[List[User], int]:
        """Fetch list of users with optional filtering."""
        query = db.query(User)
        if search:
            search_term = f"%{search.strip().lower()}%"
            query = query.filter(
                or_(
                    func.lower(User.full_name).like(search_term),
                    func.lower(User.email).like(search_term)
                )
            )
        total = query.count()
        users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
        return users, total

    @staticmethod
    def update_user_status(
        db: Session,
        target_user_id: int,
        is_active: bool,
        current_admin: User,
        client_ip: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> User:
        """Suspend or activate user account."""
        if target_user_id == current_admin.id and not is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Administrators cannot deactivate their own accounts."
            )

        target_user = db.query(User).filter(User.id == target_user_id).first()
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        target_user.is_active = is_active
        target_user.updated_at = utc_now()
        db.commit()

        AuthService.log_audit_event(
            db,
            event_type="ADMIN_UPDATE_STATUS",
            user_id=current_admin.id,
            ip_address=client_ip,
            user_agent=user_agent,
            details=f"Admin {current_admin.email} set status of user {target_user.email} (id {target_user.id}) to is_active={is_active}"
        )

        return target_user

    @staticmethod
    def update_user_role(
        db: Session,
        target_user_id: int,
        new_role: str,
        current_admin: User,
        client_ip: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> User:
        """Update role between user and admin."""
        if target_user_id == current_admin.id and new_role != "admin":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Administrators cannot demote their own role."
            )

        target_user = db.query(User).filter(User.id == target_user_id).first()
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        target_user.role = new_role
        target_user.updated_at = utc_now()
        db.commit()

        AuthService.log_audit_event(
            db,
            event_type="ADMIN_UPDATE_ROLE",
            user_id=current_admin.id,
            ip_address=client_ip,
            user_agent=user_agent,
            details=f"Admin {current_admin.email} updated role of user {target_user.email} (id {target_user.id}) to role={new_role}"
        )

        return target_user

    @staticmethod
    def bootstrap_first_admin(
        db: Session,
        email: str,
        password: str,
        name: str = "System Administrator"
    ) -> User:
        """
        Idempotent provisioning of the initial administrator account.
        Used via CLI bootstrap or environment variables on launch.
        """
        normalized_email = email.strip().lower()
        existing = db.query(User).filter(func.lower(User.email) == normalized_email).first()
        if existing:
            # If user already exists, elevate to admin
            if existing.role != "admin":
                existing.role = "admin"
                existing.is_active = True
                existing.is_email_verified = True
                db.commit()
                logger.info("Elevated existing user %s to admin role.", normalized_email)
            return existing

        admin = User(
            full_name=name.strip(),
            email=normalized_email,
            password_hash=get_password_hash(password),
            role="admin",
            is_active=True,
            is_email_verified=True,
            failed_login_attempts=0,
            created_at=utc_now(),
            updated_at=utc_now()
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        logger.info("Successfully bootstrapped initial admin account: %s", normalized_email)
        return admin


admin_service = AdminService()
