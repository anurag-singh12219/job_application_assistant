from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from core.config import settings
from core.database import get_db
from core.rate_limiter import get_client_ip, rate_limit_endpoint
from core.security import generate_csrf_token
from db.models import User
from schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    VerifyEmailRequest,
    ResendVerificationRequest,
    ChangePasswordRequest,
    UserResponse,
    MessageResponse,
    AuthSuccessResponse
)
from services.auth_service import AuthService
from api.deps import (
    get_current_active_user,
    verify_csrf_protection
)

router = APIRouter()


def set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: str,
    csrf_token: str,
    remember_me: bool = False
):
    """Set secure HttpOnly cookies for access and refresh tokens, plus CSRF cookie."""
    access_max_age = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    refresh_max_age = (settings.REFRESH_TOKEN_EXPIRE_DAYS if remember_me else 1) * 86400

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        path="/",
        max_age=access_max_age
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        path="/api/auth",
        max_age=refresh_max_age
    )
    # Anti-CSRF cookie is readable by frontend JavaScript to attach to mutation headers
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        path="/",
        max_age=refresh_max_age
    )


def clear_auth_cookies(response: Response):
    """Wipe authentication and CSRF cookies on logout."""
    response.delete_cookie(
        key="access_token",
        domain=settings.COOKIE_DOMAIN,
        path="/"
    )
    response.delete_cookie(
        key="refresh_token",
        domain=settings.COOKIE_DOMAIN,
        path="/api/auth"
    )
    response.delete_cookie(
        key="csrf_token",
        domain=settings.COOKIE_DOMAIN,
        path="/"
    )


@router.get("/csrf-token", response_model=MessageResponse)
async def get_csrf_token(response: Response):
    """Retrieve or initialize CSRF token for the frontend client."""
    csrf_val = generate_csrf_token()
    response.set_cookie(
        key="csrf_token",
        value=csrf_val,
        httponly=False,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        path="/",
        max_age=86400 * 7
    )
    return {"message": "CSRF token initialized", "detail": csrf_val}


@router.post(
    "/register",
    response_model=AuthSuccessResponse,
    dependencies=[Depends(rate_limit_endpoint("register", settings.RATE_LIMIT_REGISTER_PER_MINUTE, 60))]
)
async def register(
    req: UserRegisterRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Register a new account. Does not permit public admin creation."""
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent")
    user, _ = AuthService.register_user(db, req, client_ip=client_ip, user_agent=user_agent)
    
    return {
        "message": "Registration successful. Please check your email to verify your account.",
        "user": user,
        "csrf_token": None
    }


@router.post(
    "/login",
    response_model=AuthSuccessResponse,
    dependencies=[Depends(rate_limit_endpoint("login", settings.RATE_LIMIT_LOGIN_PER_MINUTE, 60))]
)
async def login(
    req: UserLoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Authenticate with email and password, returning secure session cookies."""
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent")
    user = AuthService.authenticate_user(
        db,
        email=req.email,
        password=req.password,
        client_ip=client_ip,
        user_agent=user_agent
    )

    access_token, refresh_token, csrf_token = AuthService.create_session(
        db,
        user=user,
        remember_me=bool(req.remember_me)
    )

    set_auth_cookies(
        response,
        access_token=access_token,
        refresh_token=refresh_token,
        csrf_token=csrf_token,
        remember_me=bool(req.remember_me)
    )

    return {
        "message": "Login successful.",
        "user": user,
        "csrf_token": csrf_token,
        "access_token": access_token
    }


@router.post("/logout", response_model=MessageResponse)
async def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Invalidate server-side refresh session and clear cookies."""
    raw_refresh = request.cookies.get("refresh_token")
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent")
    
    AuthService.revoke_session(
        db,
        raw_refresh_token=raw_refresh,
        client_ip=client_ip,
        user_agent=user_agent
    )
    clear_auth_cookies(response)
    return {"message": "Logged out successfully."}


@router.post(
    "/refresh",
    response_model=AuthSuccessResponse,
    dependencies=[Depends(rate_limit_endpoint("refresh", 30, 60))]
)
async def refresh_session(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Rotate refresh token and issue a fresh access token."""
    raw_refresh = request.cookies.get("refresh_token")
    if not raw_refresh:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token cookie provided."
        )

    client_ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent")

    new_access, new_refresh, new_csrf, user = AuthService.refresh_session(
        db,
        raw_refresh_token=raw_refresh,
        client_ip=client_ip,
        user_agent=user_agent
    )

    set_auth_cookies(
        response,
        access_token=new_access,
        refresh_token=new_refresh,
        csrf_token=new_csrf,
        remember_me=True
    )

    return {
        "message": "Session refreshed.",
        "user": user,
        "csrf_token": new_csrf,
        "access_token": new_access
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """Retrieve authenticated user's profile."""
    return current_user


@router.post(
    "/forgot-password",
    response_model=MessageResponse,
    dependencies=[Depends(rate_limit_endpoint("forgot-password", settings.RATE_LIMIT_PASSWORD_RESET_PER_MINUTE, 60))]
)
async def forgot_password(
    req: ForgotPasswordRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Initiate password reset. Always returns a generic response to prevent email enumeration."""
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent")
    AuthService.request_password_reset(
        db,
        email=req.email,
        client_ip=client_ip,
        user_agent=user_agent
    )
    return {
        "message": "If an account with that email exists, password reset instructions have been sent."
    }


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    dependencies=[Depends(rate_limit_endpoint("reset-password", 5, 60))]
)
async def reset_password(
    req: ResetPasswordRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Reset account password using single-use token and revoke all active sessions."""
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent")
    AuthService.reset_password(
        db,
        raw_token=req.token,
        new_password=req.password,
        client_ip=client_ip,
        user_agent=user_agent
    )
    clear_auth_cookies(response)
    return {
        "message": "Your password has been successfully reset. Please log in with your new password."
    }


@router.post(
    "/verify-email",
    response_model=MessageResponse,
    dependencies=[Depends(rate_limit_endpoint("verify-email", 10, 60))]
)
async def verify_email(
    req: VerifyEmailRequest,
    db: Session = Depends(get_db)
):
    """Confirm user email address using one-time verification token."""
    AuthService.verify_email(db, raw_token=req.token)
    return {"message": "Email address verified successfully. You may now enjoy full account features."}


@router.post(
    "/resend-verification",
    response_model=MessageResponse,
    dependencies=[Depends(rate_limit_endpoint("resend-verification", 5, 60))]
)
async def resend_verification(
    req: ResendVerificationRequest,
    db: Session = Depends(get_db)
):
    """Resend email verification link."""
    AuthService.resend_verification_email(db, email=req.email)
    return {
        "message": "If this email belongs to an unverified account, a verification link has been sent."
    }


@router.patch(
    "/change-password",
    response_model=MessageResponse,
    dependencies=[Depends(verify_csrf_protection)]
)
async def change_password(
    req: ChangePasswordRequest,
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Change password for the logged-in user and revoke existing sessions."""
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent")
    AuthService.change_password(
        db,
        user=current_user,
        current_password=req.current_password,
        new_password=req.new_password,
        client_ip=client_ip,
        user_agent=user_agent
    )
    # Clear cookies so user signs in afresh
    clear_auth_cookies(response)
    return {
        "message": "Password changed successfully. Please log in with your new credentials."
    }
