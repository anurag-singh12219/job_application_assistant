from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from core.config import settings
from core.security import (
    get_password_hash,
    verify_password,
    generate_secure_token,
    hash_token,
    generate_csrf_token,
    create_access_token
)
from db.models import (
    User,
    RefreshToken,
    EmailVerificationToken,
    PasswordResetToken,
    SecurityAuditLog
)
from schemas.auth import UserRegisterRequest
from services.email_service import email_service


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def ensure_utc(dt: Optional[datetime]) -> Optional[datetime]:
    """Ensure datetime has UTC timezone for cross-dialect compatibility (e.g. SQLite)."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


class AuthService:
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Case-insensitive user lookup by normalized email."""
        return db.query(User).filter(func.lower(User.email) == email.strip().lower()).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def log_audit_event(
        db: Session,
        event_type: str,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[str] = None
    ) -> None:
        """Record security audit log entry."""
        audit_entry = SecurityAuditLog(
            user_id=user_id,
            event_type=event_type,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details,
            created_at=utc_now()
        )
        db.add(audit_entry)
        try:
            db.commit()
        except Exception:
            db.rollback()

    @classmethod
    def register_user(
        cls,
        db: Session,
        req: UserRegisterRequest,
        client_ip: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Tuple[User, str]:
        """Register a new user account with default user role and send verification email."""
        normalized_email = req.email.strip().lower()
        
        # Check if email already registered (case-insensitive)
        existing = cls.get_user_by_email(db, normalized_email)
        if existing:
            # Generic response to prevent account enumeration
            cls.log_audit_event(
                db,
                event_type="REGISTER_DUPLICATE_ATTEMPT",
                ip_address=client_ip,
                user_agent=user_agent,
                details=f"Registration attempted for existing email."
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to complete registration with this email address. If you already have an account, please log in or reset your password."
            )

        # Create user with least-privileged role 'user'
        new_user = User(
            full_name=req.full_name.strip(),
            email=normalized_email,
            password_hash=get_password_hash(req.password),
            role="user",  # Public registration cannot assign admin role
            is_active=True,
            is_email_verified=False,
            failed_login_attempts=0,
            created_at=utc_now(),
            updated_at=utc_now()
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Create email verification token
        raw_token = generate_secure_token()
        token_hash_val = hash_token(raw_token)
        verify_token = EmailVerificationToken(
            user_id=new_user.id,
            token_hash=token_hash_val,
            expires_at=utc_now() + timedelta(hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS),
            is_used=False,
            created_at=utc_now()
        )
        db.add(verify_token)
        db.commit()

        # Audit log
        cls.log_audit_event(
            db,
            event_type="REGISTER_SUCCESS",
            user_id=new_user.id,
            ip_address=client_ip,
            user_agent=user_agent
        )

        # Send verification email
        email_service.send_verification_email(new_user.email, new_user.full_name, raw_token)

        return new_user, raw_token

    @classmethod
    def authenticate_user(
        cls,
        db: Session,
        email: str,
        password: str,
        client_ip: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> User:
        """
        Authenticate user with constant-time password check, rate limiting, and lockout protection.
        Generic failure messages are returned to prevent credential guessing.
        """
        normalized_email = email.strip().lower()
        user = cls.get_user_by_email(db, normalized_email)
        now = utc_now()

        # If user exists, check lockout status
        if user and user.locked_until and ensure_utc(user.locked_until) > now:
            cls.log_audit_event(
                db,
                event_type="LOGIN_LOCKED_ATTEMPT",
                user_id=user.id,
                ip_address=client_ip,
                user_agent=user_agent
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is temporarily locked due to multiple failed login attempts. Please try again later."
            )

        # Check credentials
        is_password_valid = False
        if user:
            is_password_valid = verify_password(password, user.password_hash)

        if not user or not is_password_valid:
            if user:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= settings.MAX_FAILED_LOGIN_ATTEMPTS:
                    user.locked_until = now + timedelta(minutes=settings.ACCOUNT_LOCKOUT_MINUTES)
                    cls.log_audit_event(
                        db,
                        event_type="ACCOUNT_LOCKED",
                        user_id=user.id,
                        ip_address=client_ip,
                        user_agent=user_agent,
                        details=f"Locked after {user.failed_login_attempts} failed attempts."
                    )
                db.commit()
                cls.log_audit_event(
                    db,
                    event_type="LOGIN_FAILED",
                    user_id=user.id,
                    ip_address=client_ip,
                    user_agent=user_agent
                )
            else:
                cls.log_audit_event(
                    db,
                    event_type="LOGIN_FAILED_UNKNOWN_EMAIL",
                    ip_address=client_ip,
                    user_agent=user_agent
                )

            # Generic failure message
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        # Check active status
        if not user.is_active:
            cls.log_audit_event(
                db,
                event_type="LOGIN_INACTIVE_ACCOUNT",
                user_id=user.id,
                ip_address=client_ip,
                user_agent=user_agent
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account has been deactivated. Please contact support."
            )

        # Reset failed attempts and update last login
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login_at = now
        db.commit()

        cls.log_audit_event(
            db,
            event_type="LOGIN_SUCCESS",
            user_id=user.id,
            ip_address=client_ip,
            user_agent=user_agent
        )

        return user

    @classmethod
    def create_session(
        cls,
        db: Session,
        user: User,
        remember_me: bool = False
    ) -> Tuple[str, str, str]:
        """
        Create access token, rotated refresh token, and anti-CSRF token.
        Returns: (access_token, raw_refresh_token, csrf_token)
        """
        now = utc_now()
        access_token = create_access_token(str(user.id), user.role)
        raw_refresh_token = generate_secure_token()
        token_hash_val = hash_token(raw_refresh_token)
        token_family = generate_secure_token()
        
        days_valid = settings.REFRESH_TOKEN_EXPIRE_DAYS if remember_me else 1
        expires_at = now + timedelta(days=days_valid)

        refresh_entry = RefreshToken(
            user_id=user.id,
            token_hash=token_hash_val,
            token_family=token_family,
            expires_at=expires_at,
            is_revoked=False,
            created_at=now
        )
        db.add(refresh_entry)
        db.commit()

        csrf_token = generate_csrf_token()
        return access_token, raw_refresh_token, csrf_token

    @classmethod
    def refresh_session(
        cls,
        db: Session,
        raw_refresh_token: str,
        client_ip: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Tuple[str, str, str, User]:
        """
        Rotate refresh token with reuse detection.
        Returns: (new_access_token, new_raw_refresh_token, new_csrf_token, user)
        """
        now = utc_now()
        token_hash_val = hash_token(raw_refresh_token)
        token_entry = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash_val).first()

        if not token_entry or ensure_utc(token_entry.expires_at) < now:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired or invalid. Please sign in again."
            )

        # Reuse Detection: If an already-revoked refresh token is used, compromise is suspected!
        if token_entry.is_revoked:
            # Revoke all tokens in the same family immediately
            db.query(RefreshToken).filter(RefreshToken.token_family == token_entry.token_family).update(
                {"is_revoked": True}
            )
            db.commit()
            cls.log_audit_event(
                db,
                event_type="REFRESH_TOKEN_REUSE_DETECTED",
                user_id=token_entry.user_id,
                ip_address=client_ip,
                user_agent=user_agent,
                details=f"Compromised refresh token family {token_entry.token_family} revoked."
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Security alert: Session anomaly detected. Please sign in again."
            )

        user = token_entry.user
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive."
            )

        # Invalidate current refresh token
        token_entry.is_revoked = True

        # Generate new rotated refresh token in the same family
        new_raw_refresh_token = generate_secure_token()
        new_token_hash = hash_token(new_raw_refresh_token)
        token_entry.replaced_by = new_token_hash

        new_token_entry = RefreshToken(
            user_id=user.id,
            token_hash=new_token_hash,
            token_family=token_entry.token_family,
            expires_at=token_entry.expires_at,  # maintain overall session horizon
            is_revoked=False,
            created_at=now
        )
        db.add(new_token_entry)
        db.commit()

        new_access_token = create_access_token(str(user.id), user.role)
        new_csrf_token = generate_csrf_token()

        cls.log_audit_event(
            db,
            event_type="TOKEN_REFRESH_SUCCESS",
            user_id=user.id,
            ip_address=client_ip,
            user_agent=user_agent
        )

        return new_access_token, new_raw_refresh_token, new_csrf_token, user

    @classmethod
    def revoke_session(
        cls,
        db: Session,
        raw_refresh_token: Optional[str] = None,
        user_id: Optional[int] = None,
        client_ip: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> None:
        """Revoke refresh token session on logout."""
        if raw_refresh_token:
            token_hash_val = hash_token(raw_refresh_token)
            token_entry = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash_val).first()
            if token_entry:
                token_entry.is_revoked = True
                db.commit()
        
        cls.log_audit_event(
            db,
            event_type="LOGOUT",
            user_id=user_id,
            ip_address=client_ip,
            user_agent=user_agent
        )

    @classmethod
    def verify_email(cls, db: Session, raw_token: str) -> User:
        """Verify user's email address using one-time verification token."""
        token_hash_val = hash_token(raw_token)
        now = utc_now()
        token_entry = db.query(EmailVerificationToken).filter(
            EmailVerificationToken.token_hash == token_hash_val
        ).first()

        if not token_entry or token_entry.is_used or ensure_utc(token_entry.expires_at) < now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification link is invalid, expired, or has already been used."
            )

        token_entry.is_used = True
        user = token_entry.user
        user.is_email_verified = True
        user.updated_at = now
        db.commit()

        cls.log_audit_event(
            db,
            event_type="EMAIL_VERIFIED",
            user_id=user.id
        )

        return user

    @classmethod
    def resend_verification_email(cls, db: Session, email: str) -> None:
        """Generate a new verification token and email it (generic response)."""
        normalized_email = email.strip().lower()
        user = cls.get_user_by_email(db, normalized_email)
        
        if user and not user.is_email_verified:
            # Invalidate older unused tokens
            db.query(EmailVerificationToken).filter(
                EmailVerificationToken.user_id == user.id,
                EmailVerificationToken.is_used == False
            ).update({"is_used": True})
            
            raw_token = generate_secure_token()
            token_entry = EmailVerificationToken(
                user_id=user.id,
                token_hash=hash_token(raw_token),
                expires_at=utc_now() + timedelta(hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS),
                is_used=False,
                created_at=utc_now()
            )
            db.add(token_entry)
            db.commit()
            email_service.send_verification_email(user.email, user.full_name, raw_token)

    @classmethod
    def request_password_reset(
        cls,
        db: Session,
        email: str,
        client_ip: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> None:
        """Initiate password reset flow without revealing account existence."""
        normalized_email = email.strip().lower()
        user = cls.get_user_by_email(db, normalized_email)
        
        if user and user.is_active:
            # Invalidate previous unused reset tokens
            db.query(PasswordResetToken).filter(
                PasswordResetToken.user_id == user.id,
                PasswordResetToken.is_used == False
            ).update({"is_used": True})

            raw_token = generate_secure_token()
            token_entry = PasswordResetToken(
                user_id=user.id,
                token_hash=hash_token(raw_token),
                expires_at=utc_now() + timedelta(hours=settings.PASSWORD_RESET_EXPIRE_HOURS),
                is_used=False,
                created_at=utc_now()
            )
            db.add(token_entry)
            db.commit()

            cls.log_audit_event(
                db,
                event_type="PASSWORD_RESET_REQUESTED",
                user_id=user.id,
                ip_address=client_ip,
                user_agent=user_agent
            )

            email_service.send_password_reset_email(user.email, user.full_name, raw_token)

    @classmethod
    def reset_password(
        cls,
        db: Session,
        raw_token: str,
        new_password: str,
        client_ip: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> User:
        """Complete password reset and revoke all existing sessions."""
        token_hash_val = hash_token(raw_token)
        now = utc_now()
        token_entry = db.query(PasswordResetToken).filter(
            PasswordResetToken.token_hash == token_hash_val
        ).first()

        if not token_entry or token_entry.is_used or ensure_utc(token_entry.expires_at) < now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password reset link is invalid, expired, or has already been used."
            )

        token_entry.is_used = True
        user = token_entry.user
        user.password_hash = get_password_hash(new_password)
        user.failed_login_attempts = 0
        user.locked_until = None
        user.updated_at = now

        # Revoke all existing sessions for security
        db.query(RefreshToken).filter(RefreshToken.user_id == user.id).update({"is_revoked": True})
        db.commit()

        cls.log_audit_event(
            db,
            event_type="PASSWORD_RESET_COMPLETED",
            user_id=user.id,
            ip_address=client_ip,
            user_agent=user_agent
        )

        return user

    @classmethod
    def change_password(
        cls,
        db: Session,
        user: User,
        current_password: str,
        new_password: str,
        client_ip: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> None:
        """Change user password after verifying current credentials; revokes other sessions."""
        if not verify_password(current_password, user.password_hash):
            cls.log_audit_event(
                db,
                event_type="PASSWORD_CHANGE_FAILED",
                user_id=user.id,
                ip_address=client_ip,
                user_agent=user_agent
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect."
            )

        user.password_hash = get_password_hash(new_password)
        user.updated_at = utc_now()

        # Revoke existing refresh tokens
        db.query(RefreshToken).filter(RefreshToken.user_id == user.id).update({"is_revoked": True})
        db.commit()

        cls.log_audit_event(
            db,
            event_type="PASSWORD_CHANGE_SUCCESS",
            user_id=user.id,
            ip_address=client_ip,
            user_agent=user_agent
        )
